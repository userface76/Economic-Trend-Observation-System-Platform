import httpx

from app.config import settings


BASE_URL = "https://ecos.bok.or.kr/api/StatisticSearch"


async def fetch_statistic(stat_code: str, item_code: str, start: str, end: str) -> list[dict]:
    if not settings.ecos_api_key:
        return []
    url = f"{BASE_URL}/{settings.ecos_api_key}/json/kr/1/100/{stat_code}/M/{start}/{end}/{item_code}"
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json().get("StatisticSearch", {}).get("row", [])

