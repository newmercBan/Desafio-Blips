import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ExternalService:
    @staticmethod
    async def get_birth_date() -> str | None:
        """
        Fetches birthDate from external API.
        Returns the date string (e.g., '1996-5-30') or None if request fails.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(settings.EXTERNAL_API_URL, timeout=5.0)
                response.raise_for_status()
                data = response.json()
                # API returns "birthDate": "1996-5-30" or similar
                # Requirement example says output "1998-02-05", input format might vary.
                # dummyjson returns "YYYY-M-D" often.
                # We will return it as is or normalize if needed.
                # For now, return raw string from API.
                return data.get("birthDate")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling external API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling external API: {e}")
            return None
