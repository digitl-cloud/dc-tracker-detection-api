from pydantic import BaseModel, field_validator
import re


class AnalyzeRequest(BaseModel):
    """API request for tracker analysis."""
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Clean and validate domain."""
        v = v.strip().lower()
        v = re.sub(r'^https?://', '', v)  # Remove protocol
        v = re.sub(r'/.*$', '', v)         # Remove path
        v = re.sub(r'^www\.', '', v)       # Remove www

        # Validate domain format
        pattern = r"^[a-zA-Z0-9][a-zA-Z0-9\-_.]*\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError(f"Invalid domain: {v}")
        return v


class TrackerEvidence(BaseModel):
    """Single detected tracker with evidence."""
    name: str                    # "Google Analytics 4"
    category: str                # "analytics"
    evidence: list[str]          # ["Script: https://...", "Network: ..."]
    confidence: str              # "high" | "medium" | "low"
    competitor_priority: str     # "high" | "medium" | "low" | "self"
    example_url: str | None      # First HTTP URL from evidence (for manual check)


class AnalyzeResponse(BaseModel):
    """API response with all detected trackers."""
    domain: str                        # Cleaned domain
    total_detected: int                # Total tracker count
    all_trackers: list[TrackerEvidence]  # Complete tracker list
    metadata: dict                     # Crawl statistics
    crawl_status: str                  # "success" | "partial" | "failed"
    error_message: str | None          # Error details if failed/partial
