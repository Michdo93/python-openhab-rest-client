from .client import OpenHABClient


class Iconsets:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Iconsets-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_iconsets(self, language: str = None) -> list:
        """
        Ruft alle verfügbaren Iconsets ab.

        :param language: Optionale Sprachpräferenz für die Antwort (z. B. 'en', 'de').
        :return: Eine Liste von Iconsets mit Details wie ID, Label, Beschreibung und unterstützten Formaten.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/iconsets"
        headers = {"Accept-Language": language} if language else {}
        
        try:
            return self.client.get(endpoint, headers=headers)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der Iconsets: {e}")
