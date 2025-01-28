from .client import OpenHABClient

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
        return self.client.post(f"/ui/components/{namespace}", json=component_data)

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
        return self.client.put(f"/ui/components/{namespace}/{component_uid}", json=component_data)

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


"""

from client import OpenHABClient
from ui import UI

# OpenHABClient instanziieren
client = OpenHABClient(base_url="http://your-openhab-instance:8080")
ui = UI(client)

# Alle UI-Komponenten im Namespace "home" abrufen
namespace = "home"
ui_components = ui.get_ui_components(namespace)
print(ui_components)

# Eine neue UI-Komponente hinzufügen
component_data = {
    "component": "Button",
    "config": {
        "label": "Turn On Light",
        "action": "turn_on"
    },
    "slots": {
        "slot1": [{"component": "Icon", "config": {"icon": "light"}}]
    },
    "uid": "unique-button-uid",
    "tags": ["button", "light-control"],
    "props": {
        "uri": "/control/light",
        "parameters": [
            {"name": "light", "label": "Light", "type": "TEXT", "required": True}
        ]
    },
    "timestamp": "2025-01-27T15:37:35.741Z",
    "type": "button"
}
new_component = ui.add_ui_component(namespace, component_data)
print(new_component)

# Eine spezifische UI-Komponente abrufen
component_uid = "unique-button-uid"
component = ui.get_ui_component(namespace, component_uid)
print(component)

# Eine UI-Komponente aktualisieren
updated_component_data = {
    "component": "Button",
    "config": {
        "label": "Turn Off Light",
        "action": "turn_off"
    },
    "uid": "unique-button-uid"
}
updated_component = ui.update_ui_component(namespace, component_uid, updated_component_data)
print(updated_component)

# Eine UI-Komponente löschen
deleted_component = ui.delete_ui_component(namespace, component_uid)
print(deleted_component)

# Alle UI-Kacheln abrufen
ui_tiles = ui.get_ui_tiles()
print(ui_tiles)


"""