import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_analyze_valid_domain():
    """Test analyzing a valid domain."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/analyze",
            json={"url": "example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "domain" in data
        assert "total_detected" in data
        assert "all_trackers" in data
        assert data["crawl_status"] in ["success", "partial", "failed"]


@pytest.mark.asyncio
async def test_analyze_invalid_domain():
    """Test analyzing an invalid domain format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/analyze",
            json={"url": "invalid domain!"}
        )
        assert response.status_code == 422  # Validation error
