from .client import OpenHABClient
import json

class Actions:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Actions-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_actions(self, thing_uid: str, language: str = None) -> list:
        """
        Ruft alle verfügbaren Aktionen für den angegebenen Thing-UID ab.

        :param thing_uid: Die UID des Things, für das Aktionen abgerufen werden sollen.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Aktionen.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = f"/actions/{thing_uid}"
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)

    def execute_action(self, thing_uid: str, action_uid: str, action_inputs: dict, language: str = None) -> str:
        """
        Führt eine spezifische Aktion für das angegebene Thing aus.

        :param thing_uid: Die UID des Things, auf dem die Aktion ausgeführt werden soll.
        :param action_uid: Die UID der auszuführenden Aktion.
        :param action_inputs: Die Eingaben für die Aktion als Dictionary.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Antwort vom Server.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = f"/actions/{thing_uid}/{action_uid}"
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        # Sicherstellen, dass action_inputs korrekt serialisiert wird
        try:
            action_inputs_json = json.dumps(action_inputs)
        except TypeError as e:
            raise ValueError(f"Fehler bei der Serialisierung des action_inputs-Dictionaries: {e}")

        print(action_inputs_json)

        return self.client.post(endpoint, header=header, data=action_inputs_json)
