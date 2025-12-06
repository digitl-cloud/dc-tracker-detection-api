from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.models import AnalyzeRequest, AnalyzeResponse, TrackerEvidence
from app.services.browser_crawler import browser_crawler
from app.services.tech_detector import tech_detector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI application."""
    # Startup: nothing needed (browser created on first use)
    yield
    # Shutdown: cleanup browser
    await browser_crawler.close()
    logger.info("Browser closed")


app = FastAPI(
    title="Tracker Detection API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_domain(request: AnalyzeRequest):
    """
    Analyze a domain for marketing/advertising trackers.

    Returns all detected trackers with evidence, even on partial crawl failure.
    """
    logger.info(f"Analyzing domain: {request.url}")

    # Crawl with browser (60s timeout)
    crawl_result = await browser_crawler.crawl(request.url)

    crawl_status = "success"
    error_message = None

    if not crawl_result.success:
        logger.warning(f"Crawl failed for {request.url}: {crawl_result.error_message}")
        crawl_status = "failed"
        error_message = crawl_result.error_message

        # Return empty result on complete failure
        if not crawl_result.html and not crawl_result.script_srcs:
            return AnalyzeResponse(
                domain=request.url,
                total_detected=0,
                all_trackers=[],
                metadata={
                    "consent_accepted": False,
                    "network_requests": 0,
                    "third_party_domains": 0,
                    "network_detected_count": 0
                },
                crawl_status="failed",
                error_message=error_message
            )

        # Partial data available - continue with detection
        crawl_status = "partial"

    # Detect trackers (works even with partial crawl data)
    tech_result = tech_detector.detect(request.url, crawl_result)

    # Build tracker evidence list
    all_trackers = []

    for category, tools in tech_result.detected.items():
        for tool in tools:
            # Extract example URL from evidence
            example_url = None
            for evidence_item in tool.evidence:
                if "http" in evidence_item:
                    # Extract URL from evidence string
                    if "Script: " in evidence_item:
                        example_url = evidence_item.replace("Script: ", "").strip()
                    elif "Request: " in evidence_item:
                        example_url = f"https://{evidence_item.replace('Request: ', '').strip()}"
                    elif "Network: " in evidence_item:
                        example_url = f"https://{evidence_item.replace('Network: ', '').strip()}"

                    if example_url:
                        break

            tracker = TrackerEvidence(
                name=tool.name,
                category=category,
                evidence=tool.evidence,
                confidence=tool.confidence,
                competitor_priority=tool.competitor_priority,
                example_url=example_url
            )
            all_trackers.append(tracker)

    logger.info(f"Detected {len(all_trackers)} trackers for {request.url} (status: {crawl_status})")

    return AnalyzeResponse(
        domain=request.url,
        total_detected=len(all_trackers),
        all_trackers=all_trackers,
        metadata={
            "consent_accepted": crawl_result.consent_accepted,
            "network_requests": len(crawl_result.network_requests),
            "third_party_domains": len(crawl_result.third_party_domains),
            "network_detected_count": tech_result.network_detected
        },
        crawl_status=crawl_status,
        error_message=error_message
    )
