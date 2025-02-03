from .client import OpenHABClient

class Sitemaps:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Sitemaps-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_sitemaps(self):
        """
        Holt alle verfügbaren Sitemaps.

        :return: Eine Liste von Sitemaps (JSON).
        """
        return self.client.get("/sitemaps")

    def get_sitemap(self, sitemapname: str, language=None, type=None, jsoncallback=None, include_hidden=False):
        """
        Holt eine Sitemap anhand des Namens.

        :param sitemapname: Der Name der Sitemap, die abgerufen werden soll.
        :param language: Optionale Spracheinstellung (als Header).
        :param type: Optionaler Query-Parameter für den Typ.
        :param jsoncallback: Optionaler Query-Parameter für JSON-Rückruf.
        :param include_hidden: Ob versteckte Widgets einbezogen werden sollen.

        :return: Das Sitemap-Objekt (JSON).
        """
        params = {
            "type": type,
            "jsoncallback": jsoncallback,
            "includeHidden": include_hidden
        }
        header = {"Accept-Language": language} if language else {}
        return self.client.get(f"/sitemaps/{sitemapname}", header=header, params=params)

    def get_sitemap_page(self, sitemapname: str, pageid: str, subscriptionid=None, include_hidden=False):
        """
        Holt die Daten für eine Seite einer Sitemap.

        :param sitemapname: Der Name der Sitemap.
        :param pageid: Die ID der Seite.
        :param subscriptionid: Optionaler Query-Parameter für die Subscription ID.
        :param include_hidden: Ob versteckte Widgets einbezogen werden sollen.

        :return: Die Seite der Sitemap (JSON).
        """
        params = {
            "subscriptionid": subscriptionid,
            "includeHidden": include_hidden
        }
        return self.client.get(f"/sitemaps/{sitemapname}/{pageid}", params=params)

    def get_full_sitemap(self, sitemapname: str, subscriptionid=None, include_hidden=False):
        """
        Holt alle Daten für eine ganze Sitemap.

        :param sitemapname: Der Name der Sitemap.
        :param subscriptionid: Optionaler Query-Parameter für die Subscription ID.
        :param include_hidden: Ob versteckte Widgets einbezogen werden sollen.

        :return: Die komplette Sitemap (JSON).
        """
        params = {
            "subscriptionid": subscriptionid,
            "includeHidden": include_hidden
        }
        return self.client.get(f"/sitemaps/{sitemapname}/*", params=params)

    def get_sitemap_events(self, subscriptionid: str, sitemap=None, pageid=None):
        """
        Holt Ereignisse für eine Sitemap.

        :param subscriptionid: Die ID der Subscription.
        :param sitemap: Der Name der Sitemap (optional).
        :param pageid: Die ID der Seite (optional).

        :return: Die Ereignisse (JSON).
        """
        params = {
            "sitemap": sitemap,
            "pageid": pageid
        }
        return self.client.get(f"/sitemaps/events/{subscriptionid}", params=params)

    def get_full_sitemap_events(self, subscriptionid: str, sitemap=None):
        """
        Holt Ereignisse für die gesamte Sitemap.

        :param subscriptionid: Die ID der Subscription.
        :param sitemap: Der Name der Sitemap (optional).

        :return: Die Ereignisse für die komplette Sitemap (JSON).
        """
        params = {
            "sitemap": sitemap
        }
        return self.client.get(f"/sitemaps/events/{subscriptionid}/*", params=params)

    def subscribe_to_sitemap_events(self):
        """
        Erstellt eine Sitemap-Ereignis-Subscription.

        :return: Die Antwort auf die Subscriptions-Anfrage (JSON).
        """
        return self.client.post("/sitemaps/events/subscribe")
