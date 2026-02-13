from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp


class AsyncLogging:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncLogging class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getLoggers(self) -> dict:
        """
        Get all loggers asynchronously.
        """
        try:
            response = await self.client.get("/logging", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getLogger(self, loggerName: str) -> dict:
        """
        Get a single logger asynchronously.
        """
        try:
            response = await self.client.get(f"/logging/{loggerName}", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def modifyOrAddLogger(self, loggerName: str, level: str) -> dict:
        """
        Modify or add a logger asynchronously.
        """
        data = {"loggerName": loggerName, "level": level}
        try:
            response = await self.client.put(f"/logging/{loggerName}", data=json.dumps(data), headers={"Content-Type": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Payload is invalid."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def removeLogger(self, loggerName: str) -> dict:
        """
        Remove a single logger asynchronously.
        """
        try:
            response = await self.client.delete(f"/logging/{loggerName}")
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
