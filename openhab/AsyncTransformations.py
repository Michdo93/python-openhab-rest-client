from .AsyncClient import AsyncOpenHABClient
import aiohttp
import json

class AsyncTransformations:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncTransformations class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getTransformations(self):
        """Get a list of all transformations."""
        try:
            response = await self.client.get("/transformations", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getTransformation(self, transformationUID: str):
        """Get a single transformation."""
        try:
            response = await self.client.get(f"/transformations/{transformationUID}", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateTransformation(self, transformationUID: str, transformationData):
        """Update a single transformation."""
        try:
            response = await self.client.put(
                f"/transformations/{transformationUID}",
                data=json.dumps(transformationData),
                headers={"Content-Type": "application/json"}
            )
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Bad Request (content missing or invalid)"}
            elif err.status == 405:
                return {"error": "Transformation not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteTransformation(self, transformationUID: str):
        """Delete a single transformation."""
        try:
            response = await self.client.delete(f"/transformations/{transformationUID}")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "UID not found."}
            elif err.status == 405:
                return {"error": "Transformation not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getTransformationServices(self):
        """Get all transformation services."""
        try:
            response = await self.client.get("/transformations/services", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
