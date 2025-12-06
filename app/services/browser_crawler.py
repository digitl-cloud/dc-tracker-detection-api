"""
Browser-based Crawler using Playwright.

Provides JavaScript execution, network request interception,
and automatic consent handling for accurate tracker detection.
"""
import asyncio
import logging
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from playwright_stealth import Stealth

logger = logging.getLogger(__name__)


@dataclass
class BrowserCrawlResult:
    """Result from browser-based crawling."""
    html: str
    script_srcs: list[str]
    inline_js: str
    meta_tags: dict[str, str]
    link_hrefs: list[str]
    network_requests: list[str] = field(default_factory=list)
    third_party_domains: set[str] = field(default_factory=set)
    success: bool = True
    error_message: str = ""
    consent_accepted: bool = False


# Common consent banner selectors for auto-accept
CONSENT_SELECTORS = [
    # OneTrust
    "#onetrust-accept-btn-handler",
    ".onetrust-accept-btn-handler",
    # Cookiebot
    "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
    "#CybotCookiebotDialogBodyButtonAccept",
    "a#CybotCookiebotDialogBodyLevelButtonAccept",
    # Didomi
    "#didomi-notice-agree-button",
    ".didomi-continue-without-agreeing",
    # Usercentrics
    "[data-testid='uc-accept-all-button']",
    ".uc-accept-all-button",
    # Borlabs Cookie
    "a.borlabs-cookie-btn-accept-all",
    ".borlabs-cookie-accept-btn",
    # Klaro
    ".cm-btn-accept-all",
    ".cm-btn.cm-btn-success",
    # Quantcast
    ".qc-cmp2-summary-buttons button[mode='primary']",
    ".qc-cmp-button",
    # TrustArc / TRUSTe
    ".trustarc-agree-btn",
    "#truste-consent-button",
    # Osano
    ".osano-cm-accept-all",
    # Generic patterns (language-agnostic)
    "button[id*='accept']",
    "button[id*='agree']",
    "button[id*='consent']",
    "button[class*='accept-all']",
    "button[class*='agree-all']",
    "a[id*='accept']",
    # German patterns
    "button:has-text('Alle akzeptieren')",
    "button:has-text('Akzeptieren')",
    "button:has-text('Alle annehmen')",
    "button:has-text('Zustimmen')",
    # English patterns
    "button:has-text('Accept all')",
    "button:has-text('Accept All')",
    "button:has-text('Allow all')",
    "button:has-text('I agree')",
    "button:has-text('Accept')",
]


class BrowserCrawler:
    """
    Playwright-based crawler with:
    - Real browser JavaScript execution
    - Network request interception
    - Automatic consent banner handling
    - Anti-detection measures (stealth)
    """

    def __init__(self):
        self._playwright = None
        self._browser: Browser | None = None

    async def _ensure_browser(self) -> Browser:
        """Ensure browser is launched."""
        if self._browser is None or not self._browser.is_connected():
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                ]
            )
        return self._browser

    async def crawl(self, domain: str) -> BrowserCrawlResult:
        """
        Crawl a domain using a real browser.

        Args:
            domain: Domain to crawl (e.g., "tom-tailor.eu")

        Returns:
            BrowserCrawlResult with HTML, scripts, and network requests
        """
        url = f"https://{domain}"
        network_requests: list[str] = []
        third_party_domains: set[str] = set()
        consent_accepted = False
        context = None

        try:
            browser = await self._ensure_browser()

            # Create new context with realistic settings
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="de-DE",
                timezone_id="Europe/Berlin",
            )

            page = await context.new_page()

            # Apply stealth to avoid bot detection
            stealth = Stealth()
            await stealth.apply_stealth_async(page)

            # Set up network request interception
            def handle_request(request):
                req_url = request.url
                network_requests.append(req_url)

                # Extract third-party domains
                try:
                    parsed = urlparse(req_url)
                    req_domain = parsed.netloc.lower()
                    # Check if it's a third-party domain
                    if req_domain and domain not in req_domain:
                        third_party_domains.add(req_domain)
                except Exception:
                    pass

            page.on("request", handle_request)

            # Navigate to page (60s timeout for maximum tracker detection)
            logger.info(f"Navigating to {url}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                logger.warning(f"Initial navigation warning: {e}")

            # Wait for initial scripts to load
            await asyncio.sleep(2)

            # Try to accept consent banner
            consent_accepted = await self._handle_consent(page)

            if consent_accepted:
                logger.info(f"Consent accepted for {domain}, waiting for trackers to load...")
                # Wait for trackers to load after consent
                await asyncio.sleep(3)
                try:
                    await page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass  # Timeout is okay, some sites never reach networkidle

            # Get final HTML after JavaScript execution
            html = await page.content()

            # Extract script sources from rendered DOM
            script_srcs = await page.evaluate("""
                () => Array.from(document.querySelectorAll('script[src]'))
                    .map(s => s.src)
                    .filter(src => src)
            """)

            # Extract inline JavaScript
            inline_js = await page.evaluate("""
                () => Array.from(document.querySelectorAll('script:not([src])'))
                    .map(s => s.textContent || '')
                    .join('\\n')
            """)

            # Extract meta tags
            meta_tags = await page.evaluate("""
                () => {
                    const result = {};
                    document.querySelectorAll('meta').forEach(meta => {
                        const name = meta.getAttribute('name') || meta.getAttribute('property') || '';
                        const content = meta.getAttribute('content') || '';
                        if (name && content) result[name] = content;
                    });
                    return result;
                }
            """)

            # Extract link hrefs
            link_hrefs = await page.evaluate("""
                () => Array.from(document.querySelectorAll('link[href]'))
                    .map(l => l.href)
                    .filter(href => href)
            """)

            await context.close()

            logger.info(f"Crawled {domain}: {len(script_srcs)} scripts, {len(network_requests)} requests, {len(third_party_domains)} 3rd-party domains")

            return BrowserCrawlResult(
                html=html,
                script_srcs=script_srcs,
                inline_js=inline_js,
                meta_tags=meta_tags,
                link_hrefs=link_hrefs,
                network_requests=network_requests,
                third_party_domains=third_party_domains,
                success=True,
                consent_accepted=consent_accepted
            )

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Browser crawl failed for {domain}: {error_msg}")

            # Ensure context is closed on error
            if context:
                try:
                    await context.close()
                except Exception:
                    pass

            return BrowserCrawlResult(
                html="",
                script_srcs=[],
                inline_js="",
                meta_tags={},
                link_hrefs=[],
                network_requests=network_requests,
                third_party_domains=third_party_domains,
                success=False,
                error_message=error_msg
            )

    async def _handle_consent(self, page: Page) -> bool:
        """
        Try to accept cookie consent banner.

        Returns:
            True if consent was accepted, False otherwise
        """
        for selector in CONSENT_SELECTORS:
            try:
                # Check if selector exists and is visible
                element = await page.query_selector(selector)
                if element:
                    is_visible = await element.is_visible()
                    if is_visible:
                        logger.info(f"Found consent button: {selector}")
                        await element.click()
                        await asyncio.sleep(1)  # Wait for consent to process
                        return True
            except Exception as e:
                # Selector might not match or element not clickable
                continue

        logger.debug("No consent banner found or could not accept")
        return False

    async def close(self):
        """Close browser and cleanup."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None


# Singleton instance
browser_crawler = BrowserCrawler()
