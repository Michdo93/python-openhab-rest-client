from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncSitemaps:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncSitemaps class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getSitemaps(self):
        try:
            response = await self.client.get("/sitemaps", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getSitemap(self, sitemapName: str, type: str = None, jsonCallback: str = None, includeHidden: bool = False, language: str = None):
        includeHiddenStr = "true" if includeHidden else "false"
        headers = {"Accept-Language": language} if language else {}
        params = {"type": type, "jsoncallback": jsonCallback, "includeHidden": includeHiddenStr}

        try:
            response = await self.client.get(f"/sitemaps/{sitemapName}", params=params, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getSitemapPage(self, sitemapName: str, pageID: str, subscriptionID: str = None, includeHidden: bool = False, language: str = None):
        includeHiddenStr = "true" if includeHidden else "false"
        headers = {"Accept-Language": language} if language else {}
        params = {"subscriptionID": subscriptionID, "includeHidden": includeHiddenStr}

        try:
            response = await self.client.get(f"/sitemaps/{sitemapName}/{pageID}", params=params, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Invalid subscription id has been provided."}
            elif err.status == 404:
                return {"error": "Sitemap or page does not exist, or page refers to a non-linkable widget."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getFullSitemap(self, sitemapName: str, subscriptionID: str = None, includeHidden: bool = False, language: str = None):
        includeHiddenStr = "true" if includeHidden else "false"
        headers = {"Accept-Language": language} if language else {}
        params = {"subscriptionID": subscriptionID, "includeHidden": includeHiddenStr}

        try:
            response = await self.client.get(f"/sitemaps/{sitemapName}/*", params=params, headers=headers)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Invalid subscription id has been provided."}
            elif err.status == 404:
                return {"error": "Sitemap with requested name does not exist."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getSitemapEvents(self, subscriptionID: str, sitemapName: str = None, pageID: str = None):
        params = {"sitemap": sitemapName, "pageId": pageID}
        try:
            response = await self.client.get(f"/sitemaps/events/{subscriptionID}", params=params)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Missing sitemap or page parameter, or page not linked to subscription."}
            elif err.status == 404:
                return {"error": "Subscription not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getFullSitemapEvents(self, subscriptionID: str, sitemapName: str = None):
        params = {"sitemap": sitemapName}
        try:
            response = await self.client.get(f"/sitemaps/events/{subscriptionID}/*", params=params)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Missing sitemap parameter, or sitemap not linked to subscription."}
            elif err.status == 404:
                return {"error": "Subscription not found."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def subscribeToSitemapEvents(self):
        try:
            response = await self.client.post("/sitemaps/events/subscribe")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 503:
                return {"error": "Subscriptions limit reached."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}
