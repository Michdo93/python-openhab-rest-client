import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, UI

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
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