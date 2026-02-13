from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncIconsets:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncIconsets class with an AsyncOpenHABClient object.

        :param client: An instance of AsyncOpenHABClient used for REST-API communication.
        """
        self.client = client

    async def getIconsets(self, language: str = None):
        """
        Gets all icon sets asynchronously.

        :param language: Optional language preference for the response (e.g. 'en', 'de').

        :return: A list of icon sets with details such as ID, label, description and supported formats.
        """
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/iconsets", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
