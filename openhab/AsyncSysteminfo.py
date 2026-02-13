from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncSysteminfo:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncSysteminfo class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getSystemInfo(self):
        """
        Gets information about the system.

        :return: A dictionary with system information.
        """
        try:
            response = await self.client.get("/systeminfo", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getUoMInfo(self):
        """
        Gets all supported dimensions and their system units.

        :return: A dictionary with UoM information.
        """
        try:
            response = await self.client.get("/systeminfo/uom", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
