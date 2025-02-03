from .client import OpenHABClient
import json

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
        header = {"Accept-Language": language} if language else {}
        return self.client.get("/services", header=header)

    def get_service(self, service_id: str, language=None):
        """
        Holt einen konfigurierbaren Service anhand der gegebenen Service-ID.

        :param service_id: Die ID des zu holenden Services.
        :param language: Optionale Spracheinstellung (als Header).

        :return: Das Service-Objekt (JSON).
        """
        header = {"Accept-Language": language} if language else {}
        return self.client.get(f"/services/{service_id}", header=header)

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
        config_data = json.dumps(config_data)

        return self.client.put(f"/services/{service_id}/config", data=config_data, header={"Content-type": "application/json", "Accept": "application/json"})

    def delete_service_config(self, service_id: str):
        """
        Löscht die Konfiguration eines Services und gibt die alte Konfiguration zurück.

        :param service_id: Die ID des Services.

        :return: Die alte Konfiguration des Services (JSON).
        """
        return self.client.delete(f"/services/{service_id}/config", header={"Accept": "application/json"})

    def get_service_contexts(self, service_id: str, language=None):
        """
        Holt existierende Multiple-Context-Service-Konfigurationen für die gegebene Service-ID.

        :param service_id: Die ID des Services.
        :param language: Optionale Spracheinstellung (als Header).

        :return: Eine Liste der Kontexte (JSON).
        """
        # Setze den richtigen Accept-Header auf application/json
        header = {"Accept": "application/json"}  # Default auf application/json

        # Wenn eine Sprache übergeben wird, füge auch Accept-Language hinzu
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/services/{service_id}/contexts", header=header)
