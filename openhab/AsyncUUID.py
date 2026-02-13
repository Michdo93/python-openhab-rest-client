from .Client import OpenHABClient
import aiohttp


class AsyncUUID:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the AsyncUUID class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for async REST-API communication.
        """
        self.client = client

    async def getUUID(self) -> str:
        """
        Async: A unified unique id.

        :return: The UUID as String.
        """
        headers = {"Accept": "text/plain"}
        try:
            response = await self.client.async_get("/uuid", headers=headers)

            # Wenn der Client direkt die Antwort als String liefert
            if isinstance(response, str):
                return response.strip()

            # Wenn der Client ein dict mit status liefert
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
