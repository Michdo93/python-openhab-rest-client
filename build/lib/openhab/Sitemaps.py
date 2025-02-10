from .Client import OpenHABClient

class Sitemaps:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Sitemaps class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getSitemaps(self):
        """
        Get all available sitemaps.

        :return: A list of sitemaps (JSON).
        """
        return self.client.get("/sitemaps")

    def getSitemap(self, sitemapName: str, language=None, type=None, jsonCallback=None, includeHidden=False):
        """
        Get sitemap by name.

        :param sitemapName: The name of the sitemap to retrieve.
        :param language: Optional language setting (as header).
        :param type: Optional query parameter for type.
        :param jsonCallback: Optional query parameter for JSON callback.
        :param includeHidden: Whether hidden widgets should be included.

        :return: The sitemap object (JSON).
        """
        return self.client.get(f"/sitemaps/{sitemapName}", header={"type": type, "jsoncallback": jsonCallback, "includeHidden": includeHidden}, params={"Accept-Language": language} if language else {})

    def getSitemapPage(self, sitemapName: str, pageId: str, subscriptionID=None, includeHidden=False):
        """
        Polls the data for one page of a sitemap.

        :param sitemapName: The name of the sitemap.
        :param pageId: The ID of the page.
        :param subscriptionID: Optional query parameter for the subscription ID.
        :param includeHidden: Whether hidden widgets should be included.

        :return: The sitemap page (JSON).
        """
        return self.client.get(f"/sitemaps/{sitemapName}/{pageId}", params={"subscriptionID": subscriptionID, "includeHidden": includeHidden})

    def getFullSitemap(self, sitemapName: str, subscriptionID=None, includeHidden=False):
        """
        Polls the data for a whole sitemap. Not recommended due to potentially high traffic.

        :param sitemapName: The name of the sitemap.
        :param subscriptionID: Optional query parameter for the subscription ID.
        :param includeHidden: Whether hidden widgets should be included.

        :return: The complete sitemap (JSON).
        """
        return self.client.get(f"/sitemaps/{sitemapName}/*", params={"subscriptionID": subscriptionID, "includeHidden": includeHidden})

    def getSitemapEvents(self, subscriptionID: str, sitemap=None, pageId=None):
        """
        Get sitemap events.

        :param subscriptionID: The ID of the subscription.
        :param sitemap: The name of the sitemap (optional).
        :param pageId: The ID of the page (optional).

        :return: The events (JSON).
        """
        return self.client.get(f"/sitemaps/events/{subscriptionID}", params={"sitemap": sitemap, "pageId": pageId})

    def getFullSitemapEvents(self, subscriptionID: str, sitemap=None):
        """
        Get sitemap events for a whole sitemap. Not recommended due to potentially high traffic.

        :param subscriptionID: The ID of the subscription.
        :param sitemap: The name of the sitemap (optional).

        :return: The events for the entire sitemap (JSON).
        """
        return self.client.get(f"/sitemaps/events/{subscriptionID}/*", params={"sitemap": sitemap})

    def subscribeToSitemapEvents(self):
        """
        Creates a sitemap event subscription.

        :return: The response to the subscription request (JSON).
        """
        return self.client.post("/sitemaps/events/subscribe")
