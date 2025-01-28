from .client import OpenHABClient

class UUID:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die UUID-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_uuid(self) -> str:
        """
        Ruft die eindeutige UUID von OpenHAB ab.

        :return: Die UUID als Zeichenkette.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = "/uuid"
        response = self.client.get(endpoint)

        if isinstance(response, str):  # Falls `response` ein String ist
            return response.strip()  # Entfernt mögliche Leerzeichen oder Zeilenumbrüche
        else:
            raise ValueError("Ungültige Antwort vom Client: Erwartet String.")