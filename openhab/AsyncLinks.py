from .AsyncClient import AsyncOpenHABClient
import json
from urllib.parse import quote
import aiohttp


class AsyncLinks:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncLinks class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getLinks(self, channelUID: str = None, itemName: str = None):
        """
        Gets all available links asynchronously.
        """
        params = {}
        if channelUID:
            params["channelUID"] = channelUID
        if itemName:
            params["itemName"] = itemName

        try:
            response = await self.client.get("/links", headers={"Content-Type": "application/json"}, params=params)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getLink(self, itemName: str, channelUID: str):
        """
        Retrieves an individual link asynchronously.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        try:
            response = await self.client.get(f"/links/{itemName}/{channelUID}", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Content does not match the path."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def linkItemToChannel(self, itemName: str, channelUID: str, configuration: dict):
        """
        Links an item to a channel asynchronously.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        data = {"itemName": itemName, "channelUID": channelUID, "configuration": configuration}

        try:
            response = await self.client.put(f"/links/{itemName}/{channelUID}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Content does not match the path."}
            elif err.status == 405:
                return {"error": "Link is not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def unlinkItemFromChannel(self, itemName: str, channelUID: str):
        """
        Unlinks an item from a channel asynchronously.
        """
        itemName = quote(itemName, safe="")
        channelUID = quote(channelUID, safe="")
        try:
            response = await self.client.delete(f"/links/{itemName}/{channelUID}", headers={"Content-Type": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Link not found."}
            elif err.status == 405:
                return {"error": "Link not editable."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteAllLinks(self, object: str):
        """
        Delete all links that refer to an item or thing asynchronously.
        """
        try:
            response = await self.client.delete(f"/links/{object}")
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getOrphanLinks(self):
        """
        Get orphan links asynchronously.
        """
        try:
            response = await self.client.get("/links/orphans", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def purgeUnusedLinks(self):
        """
        Remove unused/orphaned links asynchronously.
        """
        try:
            response = await self.client.post("/links/purge")
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
