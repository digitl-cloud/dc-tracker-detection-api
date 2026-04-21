<!-- gh-gl-migrate:notice-start -->
> [!IMPORTANT]
> **This repository has moved to GitLab.**
> Active development is now at **https://gitlab.com/digitl-gmbh/teams/dc/int-tracker-detection-api**.
> This GitHub copy is archived for reference only and no longer receives updates.
<!-- gh-gl-migrate:notice-end -->

# Tracker Detection API

Standalone API for detecting marketing and advertising trackers on websites.

## Local Development

```bash
# Install dependencies
pip install -e .
playwright install chromium

# Run server
uvicorn app.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "tom-tailor.eu"}'
```

## Cloud Run Deployment

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/tracker-api
gcloud run deploy tracker-api \
  --image gcr.io/PROJECT_ID/tracker-api \
  --platform managed \
  --region europe-west1 \
  --memory 1Gi \
  --timeout 120s \
  --allow-unauthenticated
```

## API Usage

### Endpoint: `POST /analyze`

**Request:**
```json
{
  "url": "example.com"
}
```

**Response:**
```json
{
  "domain": "example.com",
  "total_detected": 15,
  "all_trackers": [
    {
      "name": "Google Analytics 4",
      "category": "analytics",
      "evidence": ["Script: https://www.googletagmanager.com/gtag/js"],
      "confidence": "high",
      "competitor_priority": "low",
      "example_url": "https://www.googletagmanager.com/gtag/js"
    }
  ],
  "metadata": {
    "consent_accepted": true,
    "network_requests": 120,
    "third_party_domains": 25,
    "network_detected_count": 8
  },
  "crawl_status": "success",
  "error_message": null
}
```

### Endpoint: `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

## Features

- Real browser JavaScript execution (Playwright Chromium)
- Automatic consent banner handling (OneTrust, Cookiebot, Didomi, etc.)
- Network request interception for highest confidence detection
- 2800+ tracker patterns from Ghostery TrackerDB
- 60-second crawl timeout for maximum tracker detection
- Partial results on failure (doesn't completely abort)
- Evidence URLs for manual verification

## Configuration

No environment variables required (fully self-contained).

**Optional:**
- `LOG_LEVEL` - Default: `INFO` (can set to `DEBUG` for verbose logging)
- `CORS_ORIGINS` - Default: `["*"]` (restrict in production)

## Performance

- **Crawl Time:** 60-90 seconds
- **Memory:** 150-200MB per request
- **Cold Start:** ~15 seconds (Playwright Chromium extraction)
- **Concurrent Requests:** 1 per instance (sequential crawls)
- **Tools Detected:** 15-25 on average

## Google ADK Integration

```python
import httpx

async def analyze_website_trackers(url: str) -> dict:
    """Analyze a website for marketing and advertising trackers."""
    async with httpx.AsyncClient(timeout=150.0) as client:
        response = await client.post(
            "https://tracker-api-XXXXX.run.app/analyze",
            json={"url": url}
        )
        response.raise_for_status()
        return response.json()

# Usage
result = await analyze_website_trackers("tom-tailor.eu")
print(f"Detected {result['total_detected']} trackers")

for tracker in result['all_trackers']:
    if tracker['competitor_priority'] == 'high':
        print(f"High-priority competitor: {tracker['name']}")
        print(f"  Evidence: {tracker['example_url']}")
```

## License

Internal use only 
