from .client import OpenHABClient

class Systeminfo:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die SystemInfo-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_system_info(self, language: str = None):
        """
        Ruft Informationen über das System ab.

        :return: Ein Dictionary mit Systeminformationen.
        """

        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/systeminfo", header=header)

    def get_uom_info(self, language: str = None):
        """
        Ruft alle unterstützten Dimensionen und deren Systemeinheiten ab.

        :return: Ein Dictionary mit UOM-Informationen.
        """

        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get("/systeminfo/uom", header=header)
