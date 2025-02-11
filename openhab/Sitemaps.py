from .Client import OpenHABClient
import requests


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
        try:
            response = self.client.get("/sitemaps")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

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
        if includeHidden:
            includeHidden = "true"
        else:
            includeHidden = "false"

        try:
            response = self.client.get(f"/sitemaps/{sitemapName}", header={"type": type, "jsoncallback": jsonCallback,
                                                                           "includeHidden": includeHidden}, params={"Accept-Language": language} if language else {})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

    def getSitemapPage(self, sitemapName: str, pageId: str, subscriptionID=None, includeHidden=False):
        """
        Polls the data for one page of a sitemap.

        :param sitemapName: The name of the sitemap.
        :param pageId: The ID of the page.
        :param subscriptionID: Optional query parameter for the subscription ID.
        :param includeHidden: Whether hidden widgets should be included.

        :return: The sitemap page (JSON).
        """
        if includeHidden:
            includeHidden = "true"
        else:
            includeHidden = "false"

        try:
            response = self.client.get(f"/sitemaps/{sitemapName}/{pageId}", params={
                                       "subscriptionID": subscriptionID, "includeHidden": includeHidden})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

    def getFullSitemap(self, sitemapName: str, subscriptionID=None, includeHidden=False):
        """
        Polls the data for a whole sitemap. Not recommended due to potentially high traffic.

        :param sitemapName: The name of the sitemap.
        :param subscriptionID: Optional query parameter for the subscription ID.
        :param includeHidden: Whether hidden widgets should be included.

        :return: The complete sitemap (JSON).
        """
        if includeHidden:
            includeHidden = "true"
        else:
            includeHidden = "false"

        try:
            response = self.client.get(f"/sitemaps/{sitemapName}/*", params={
                                       "subscriptionID": subscriptionID, "includeHidden": includeHidden})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

    def getSitemapEvents(self, subscriptionID: str, sitemap=None, pageId=None):
        """
        Get sitemap events.

        :param subscriptionID: The ID of the subscription.
        :param sitemap: The name of the sitemap (optional).
        :param pageId: The ID of the page (optional).

        :return: The events (JSON).
        """
        try:
            response = self.client.get(
                f"/sitemaps/events/{subscriptionID}", params={"sitemap": sitemap, "pageId": pageId})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

    def getFullSitemapEvents(self, subscriptionID: str, sitemap=None):
        """
        Get sitemap events for a whole sitemap. Not recommended due to potentially high traffic.

        :param subscriptionID: The ID of the subscription.
        :param sitemap: The name of the sitemap (optional).

        :return: The events for the entire sitemap (JSON).
        """
        try:
            response = self.client.get(
                f"/sitemaps/events/{subscriptionID}/*", params={"sitemap": sitemap})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}

    def subscribeToSitemapEvents(self):
        """
        Creates a sitemap event subscription.

        :return: The response to the subscription request (JSON).
        """
        try:
            response = self.client.post("/sitemaps/events/subscribe")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 405:
                return {"error": "Transformation cannot be deleted (Method Not Allowed)."}
            elif status_code == 404:
                return {"error": "UID not found."}
            else:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "UID not found."}
        elif status_code == 405:
            return {"error": "Transformation cannot be deleted (Method Not Allowed)."}

        return {"error": f"Unexpected response: {status_code}"}
