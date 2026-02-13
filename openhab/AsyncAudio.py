from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncAudio:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Async version of the Audio class.
        """
        self.client = client

    async def getDefaultSink(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/audio/defaultsink", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Sink not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Sink not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getDefaultSource(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/audio/defaultsource", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Source not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Service not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getSinks(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/audio/sinks", headers=headers)

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

    async def getSources(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/audio/sources", headers=headers)

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
