from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp


class AsyncTags:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncTags class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getTags(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get("/tags", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def createTag(self, tagData, language: str = None):
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.post("/tags", data=json.dumps(tagData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "The tag identifier is invalid or the tag label is missing."}
            elif err.status == 409:
                return {"error": "A tag with the same identifier already exists."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getTag(self, tagID: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.get(f"/tags/{tagID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Semantic tag not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateTag(self, tagID: str, tagData, language: str = None):
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        if language:
            headers["Accept-Language"] = language
        try:
            response = await self.client.put(f"/tags/{tagID}", data=json.dumps(tagData), headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Semantic tag not found."}
            elif err.status == 405:
                return {"error": "Semantic tag not editable."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteTag(self, tagID: str, language: str = None):
        headers = {"Accept-Language": language} if language else {}
        try:
            response = await self.client.delete(f"/tags/{tagID}", headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Semantic tag not found."}
            elif err.status == 405:
                return {"error": "Semantic tag not removable."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
