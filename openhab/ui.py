from .client import OpenHABClient
import json

class UI:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die UI-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_ui_components(self, namespace: str, summary: bool = False):
        """
        Holt alle registrierten UI-Komponenten im angegebenen Namespace.

        :param namespace: Der Namespace, für den UI-Komponenten abgerufen werden sollen.
        :param summary: Wenn True, werden nur die zusammengefassten Felder zurückgegeben.
        :return: Eine Liste der UI-Komponenten (JSON).
        """
        params = {'summary': summary} if summary else {}
        return self.client.get(f"/ui/components/{namespace}", params=params)

    def add_ui_component(self, namespace: str, component_data):
        """
        Fügt eine UI-Komponente im angegebenen Namespace hinzu.

        :param namespace: Der Namespace, in dem die UI-Komponente hinzugefügt werden soll.
        :param component_data: Die Daten der UI-Komponente (JSON), die hinzugefügt werden sollen.
        :return: Die Antwort auf die Anfrage (JSON).
        """
        header = {"Content-Type": "application/json"}
        component_data = json.dumps(component_data)

        return self.client.post(f"/ui/components/{namespace}", data=component_data, header=header)

    def get_ui_component(self, namespace: str, component_uid: str):
        """
        Holt eine spezifische UI-Komponente im angegebenen Namespace.

        :param namespace: Der Namespace, in dem die UI-Komponente gesucht wird.
        :param component_uid: Die UID der UI-Komponente, die abgerufen werden soll.
        :return: Die UI-Komponente (JSON).
        """
        return self.client.get(f"/ui/components/{namespace}/{component_uid}")

    def update_ui_component(self, namespace: str, component_uid: str, component_data):
        """
        Aktualisiert eine spezifische UI-Komponente im angegebenen Namespace.

        :param namespace: Der Namespace, in dem die UI-Komponente aktualisiert werden soll.
        :param component_uid: Die UID der UI-Komponente, die aktualisiert werden soll.
        :param component_data: Die neuen Daten der UI-Komponente (JSON).
        :return: Die Antwort auf die Anfrage (JSON).
        """
        component_data = json.dumps(component_data)

        return self.client.put(f"/ui/components/{namespace}/{component_uid}", data=component_data)

    def delete_ui_component(self, namespace: str, component_uid: str):
        """
        Löscht eine spezifische UI-Komponente im angegebenen Namespace.

        :param namespace: Der Namespace, in dem die UI-Komponente gelöscht werden soll.
        :param component_uid: Die UID der UI-Komponente, die gelöscht werden soll.
        :return: Die Antwort auf die Anfrage (JSON).
        """
        return self.client.delete(f"/ui/components/{namespace}/{component_uid}")

    def get_ui_tiles(self):
        """
        Holt alle registrierten UI-Kacheln.

        :return: Eine Liste der UI-Kacheln (JSON).
        """
        return self.client.get("/ui/tiles")