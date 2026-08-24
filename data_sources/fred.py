import httpx

from app.config import settings


BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


async def latest_observation(series_id: str) -> dict | None:
    if not settings.fred_api_key:
        return None
    params = {
        "series_id": series_id,
        "api_key": settings.fred_api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        observations = response.json().get("observations", [])
        return observations[0] if observations else None

