from dataclasses import dataclass
from app.services.browser_crawler import BrowserCrawlResult
from app.services.tech_patterns import TECH_PATTERNS, TECH_CATEGORIES, get_all_patterns


@dataclass
class DetectedTool:
    name: str
    category: str
    evidence: list[str]
    confidence: str  # "high", "medium", "low"
    competitor_priority: str  # "high", "medium", "low", "self"


@dataclass
class TechStackResult:
    domain: str
    detected: dict[str, list[DetectedTool]]
    summary: dict[str, int]  # category -> count
    network_detected: int = 0  # Count of tools detected via network requests


class TechDetector:
    """Detects tech stack from crawl results."""

    def __init__(self):
        # Load all patterns including Ghostery enhancements
        self._patterns = get_all_patterns()

    def detect(
        self,
        domain: str,
        crawl_result: BrowserCrawlResult
    ) -> TechStackResult:
        """
        Detect tech stack from crawl result.

        Args:
            domain: The domain that was crawled
            crawl_result: Result from BrowserCrawler

        Returns:
            TechStackResult with detected tools
        """
        detected: dict[str, list[DetectedTool]] = {}
        summary: dict[str, int] = {}
        network_detected = 0

        # Check if we have network data
        network_requests = crawl_result.network_requests
        third_party_domains = crawl_result.third_party_domains

        for category, tools in self._patterns.items():
            detected[category] = []
            for tool in tools:
                match = self._match_tool(
                    tool,
                    crawl_result,
                    network_requests,
                    third_party_domains
                )
                if match["detected"]:
                    detected[category].append(DetectedTool(
                        name=tool["name"],
                        category=category,
                        evidence=match["evidence"],
                        confidence=match["confidence"],
                        competitor_priority=tool.get("competitor_priority", "low")
                    ))
                    if match.get("network_match"):
                        network_detected += 1

            summary[category] = len(detected[category])

        return TechStackResult(
            domain=domain,
            detected=detected,
            summary=summary,
            network_detected=network_detected
        )

    def _match_tool(
        self,
        tool: dict,
        crawl_result: BrowserCrawlResult,
        network_requests: list[str] = None,
        third_party_domains: set[str] = None
    ) -> dict:
        """Match a tool against crawl result and network data."""
        evidence = []
        confidence_scores = []
        network_match = False

        network_requests = network_requests or []
        third_party_domains = third_party_domains or set()

        tool_domains = tool.get("domains", [])

        # === NETWORK-BASED DETECTION (highest confidence) ===
        # Check if tool's domains appear in actual network requests
        for tool_domain in tool_domains:
            tool_domain_lower = tool_domain.lower()

            # Check third-party domains set
            for req_domain in third_party_domains:
                if tool_domain_lower in req_domain:
                    evidence.append(f"Network: {req_domain}")
                    confidence_scores.append(0.98)  # Highest confidence
                    network_match = True
                    break

            # Check full request URLs
            if not network_match:
                for req_url in network_requests[:500]:  # Limit for performance
                    if tool_domain_lower in req_url.lower():
                        evidence.append(f"Request: {tool_domain}")
                        confidence_scores.append(0.95)
                        network_match = True
                        break

        # === SCRIPT SOURCE DETECTION ===
        # Domain matching in script sources
        for domain in tool_domains:
            for src in crawl_result.script_srcs:
                if domain in src.lower():
                    evidence.append(f"Script: {src[:80]}...")
                    confidence_scores.append(0.90)

        # Pattern matching in script sources
        for pattern in tool.get("patterns", []):
            pattern_lower = pattern.lower()

            for src in crawl_result.script_srcs:
                if pattern_lower in src.lower():
                    evidence.append(f"Script pattern: {pattern}")
                    confidence_scores.append(0.85)

            # Check inline JS
            if crawl_result.inline_js and pattern_lower in crawl_result.inline_js.lower():
                evidence.append(f"Inline JS: {pattern}")
                confidence_scores.append(0.75)

            # Check full HTML (fallback)
            if crawl_result.html and pattern_lower in crawl_result.html.lower():
                if f"Inline JS: {pattern}" not in evidence:
                    evidence.append(f"HTML: {pattern}")
                    confidence_scores.append(0.60)

        # Deduplicate evidence
        evidence = list(set(evidence))[:5]

        # Calculate confidence
        if confidence_scores:
            max_score = max(confidence_scores)
            confidence = "high" if max_score >= 0.85 else "medium" if max_score >= 0.70 else "low"
        else:
            confidence = "none"

        return {
            "detected": len(evidence) > 0,
            "evidence": evidence,
            "confidence": confidence if evidence else None,
            "network_match": network_match
        }

    def to_template_format(self, result: TechStackResult) -> dict[str, list[dict]]:
        """Convert detection result to Discovery Template format."""
        from app.services.tech_patterns import DISCOVERY_TEMPLATE_MAPPING

        template_result = {}

        for template_field, categories in DISCOVERY_TEMPLATE_MAPPING.items():
            tools = []
            for category in categories:
                for tool in result.detected.get(category, []):
                    notes = []
                    if tool.competitor_priority == "high":
                        notes.append("High priority competitor")
                    elif tool.competitor_priority == "self":
                        notes.append("Already using Insider")

                    tools.append({
                        "name": tool.name,
                        "notes": " | ".join(notes) if notes else "",
                        "confidence": tool.confidence
                    })

            template_result[template_field] = tools

        return template_result


tech_detector = TechDetector()
