from .client import OpenHABClient
import requests

class Services:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Services-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_services(self, language=None):
        """
        Holt alle konfigurierbaren Services.

        :param language: Optionale Spracheinstellung (als Header).

        :return: Eine Liste von Services (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.get("/services", headers=headers)

    def get_service(self, service_id: str, language=None):
        """
        Holt einen konfigurierbaren Service anhand der gegebenen Service-ID.

        :param service_id: Die ID des zu holenden Services.
        :param language: Optionale Spracheinstellung (als Header).

        :return: Das Service-Objekt (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.get(f"/services/{service_id}", headers=headers)

    def get_service_config(self, service_id: str):
        """
        Holt die Konfiguration für einen bestimmten Service anhand der Service-ID.

        :param service_id: Die ID des Services.

        :return: Die Konfiguration des Services (JSON).
        """
        return self.client.get(f"/services/{service_id}/config")

    def update_service_config(self, service_id: str, config_data: dict):
        """
        Aktualisiert die Konfiguration eines Services und gibt die alte Konfiguration zurück.

        :param service_id: Die ID des Services.
        :param config_data: Die neuen Konfigurationsdaten (als Dictionary).

        :return: Die alte Konfiguration des Services (JSON).
        """
        return self.client.put(f"/services/{service_id}/config", json=config_data)

    def delete_service_config(self, service_id: str):
        """
        Löscht die Konfiguration eines Services und gibt die alte Konfiguration zurück.

        :param service_id: Die ID des Services.

        :return: Die alte Konfiguration des Services (JSON).
        """
        return self.client.delete(f"/services/{service_id}/config")

    def get_service_contexts(self, service_id: str, language=None):
        """
        Holt existierende Multiple-Context-Service-Konfigurationen für die gegebene Service-ID.

        :param service_id: Die ID des Services.
        :param language: Optionale Spracheinstellung (als Header).

        :return: Eine Liste der Kontexte (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.get(f"/services/{service_id}/contexts", headers=headers)
