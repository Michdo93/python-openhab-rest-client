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
        """
        endpoint = "/addons"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.get(endpoint, header=header, params=params)

    def get_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Holt ein bestimmtes Add-on basierend auf der Addon-ID.
        """
        endpoint = f"/addons/{addon_id}"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.get(endpoint, header=header, params=params)

    def install_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Installiert das Add-on mit der gegebenen Addon-ID.
        """
        endpoint = f"/addons/{addon_id}/install"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.post(endpoint, header=header, json=params)

    def uninstall_addon(self, addon_id: str, service_id: str = None, language: str = None) -> dict:
        """
        Deinstalliert das Add-on mit der gegebenen Addon-ID.
        """
        endpoint = f"/addons/{addon_id}/uninstall"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.post(endpoint, header=header, json=params)

    def get_addon_types(self, language: str = None) -> dict:
        """
        Holt alle Add-on Typen von OpenHAB.
        """
        endpoint = "/addons/types"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.get(endpoint, header=header, params=None)

    def get_addon_suggestions(self, language: str = None) -> dict:
        """
        Holt empfohlene Add-ons, die installiert werden können.
        """
        endpoint = "/addons/suggestions"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.get(endpoint, header=header, params=None)

    def get_addon_config(self, addon_id: str, service_id: str = None) -> dict:
        """
        Holt die Konfiguration eines Add-ons basierend auf der Addon-ID.
        """
        endpoint = f"/addons/{addon_id}/config"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        return self.client.get(endpoint, header=header, params=params)

    def update_addon_config(self, addon_id: str, config_data: dict, service_id: str = None) -> dict:
        """
        Aktualisiert die Konfiguration eines Add-ons und gibt die alte Konfiguration zurück.
        """
        endpoint = f"/addons/{addon_id}/config"
        params = {"serviceId": service_id} if service_id else {}
        header = {"Content-Type": "application/json"}
        return self.client.put(endpoint, header=header, json=config_data, params=params)

    def get_addon_services(self, language: str = None) -> dict:
        """
        Holt alle verfügbaren Add-on Services.
        """
        endpoint = "/addons/services"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        return self.client.get(endpoint, header=header, params=None)

    def install_addon_from_url(self, url: str) -> dict:
        """
        Installiert ein Add-on von der angegebenen URL.

        :param url: URL des Add-ons, das installiert werden soll
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/addons/url/{url}/install"
        header = {"Content-Type": "application/json"}
        return self.client.post(endpoint, header=header, json=None)