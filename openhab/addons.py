import json
from .client import OpenHABClient

class Addons:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Addons-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client  

    def get_addons(self, service_id: str = None, language: str = None) -> dict:
        """
        Holt alle Add-ons von OpenHAB.

        :param service_id: (Optional) ID des Dienstes, um Add-ons für diesen Dienst zu erhalten
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/addons"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        # Statt 'data' sollten wir 'params' verwenden, wenn es Query-Parameter sind
        return self.client.get(endpoint, header=header, params=params)

    def get_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Holt ein bestimmtes Add-on basierend auf der Addon-ID.

        :param addon_id: ID des Add-ons
        :param service_id: (Optional) ID des Dienstes
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/addons/{addon_id}"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        # Wenn Daten vorhanden sind, diese in JSON umwandeln
        params = json.dumps(params) if params else None

        return self.client.get(endpoint, header=header, params=params)

    def install_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Installiert das Add-on mit der gegebenen Addon-ID.

        :param addon_id: ID des Add-ons
        :param service_id: (Optional) ID des Dienstes
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/addons/{addon_id}/install"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        # Wenn Daten vorhanden sind, diese in JSON umwandeln
        data = json.dumps(params) if params else None

        return self.client.post(endpoint, header=header, data=data)

    def uninstall_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Deinstalliert das Add-on mit der gegebenen Addon-ID.

        :param addon_id: ID des Add-ons
        :param service_id: (Optional) ID des Dienstes
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/addons/{addon_id}/uninstall"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        # Wenn Daten vorhanden sind, diese in JSON umwandeln
        data = json.dumps(params) if params else None

        return self.client.post(endpoint, header=header, data=data)

    def get_addon_types(self, language: str = None) -> dict:
        """
        Holt alle Add-on Typen von OpenHAB.

        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = "/addons/types"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header, params=None)

    def get_addon_suggestions(self, language: str = None) -> dict:
        """
        Holt empfohlene Add-ons, die installiert werden können.

        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = "/addons/suggestions"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header, params=None)
