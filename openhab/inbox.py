from .client import OpenHABClient


class Inbox:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Inbox-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_discovered_things(self, include_ignored: bool = True) -> list:
        """
        Ruft alle entdeckten Dinge aus der Inbox ab.

        :param include_ignored: Ob auch ignorierte Einträge einbezogen werden sollen (Standard: True).
        :return: Eine Liste von entdeckten Dingen mit Details wie UID, Flag, Label und Eigenschaften.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/inbox"
        params = {"includeIgnored": str(include_ignored).lower()}
        
        try:
            return self.client.get(endpoint, params=params)
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen der entdeckten Dinge: {e}")

    def remove_discovery_result(self, thing_uid: str) -> dict:
        """
        Entfernt ein Entdeckungsergebnis aus der Inbox.

        :param thing_uid: Die UID des entdeckten Geräts, das entfernt werden soll.
        :return: Die Antwort der API auf die Löschanfrage.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/inbox/{thing_uid}"
        
        try:
            return self.client.delete(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Entfernen des Entdeckungsergebnisses: {e}")

    def approve_discovery_result(self, thing_uid: str, thing_label: str, new_thing_id: str = None, language: str = None) -> dict:
        """
        Genehmigt ein Entdeckungsergebnis und fügt das Thing zum Registry hinzu.

        :param thing_uid: Die UID des entdeckten Geräts.
        :param thing_label: Der neue Name des Geräts.
        :param new_thing_id: Optional: Die neue Thing-ID.
        :param language: Optional: Sprachpräferenz für die Antwort.
        :return: Die Antwort der API auf die Genehmigungsanfrage.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/inbox/{thing_uid}/approve"
        headers = {"Accept-Language": language} if language else {}
        params = {"newThingId": new_thing_id} if new_thing_id else {}
        data = {"thing label": thing_label}
        
        try:
            return self.client.post(endpoint, headers=headers, params=params, json=data)
        except Exception as e:
            raise Exception(f"Fehler bei der Genehmigung des Entdeckungsergebnisses: {e}")

    def ignore_discovery_result(self, thing_uid: str) -> dict:
        """
        Markiert ein Entdeckungsergebnis als ignoriert.

        :param thing_uid: Die UID des entdeckten Geräts.
        :return: Die Antwort der API auf die Ignorier-Anfrage.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/inbox/{thing_uid}/ignore"
        
        try:
            return self.client.post(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Ignorieren des Entdeckungsergebnisses: {e}")

    def unignore_discovery_result(self, thing_uid: str) -> dict:
        """
        Entfernt das Ignorier-Flag von einem Entdeckungsergebnis.

        :param thing_uid: Die UID des entdeckten Geräts.
        :return: Die Antwort der API auf die Unignore-Anfrage.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/inbox/{thing_uid}/unignore"
        
        try:
            return self.client.post(endpoint)
        except Exception as e:
            raise Exception(f"Fehler beim Entfernen des Ignorier-Flags: {e}")
