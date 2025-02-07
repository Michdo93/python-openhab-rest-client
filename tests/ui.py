import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, UI

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
uiApi = UI(client)

# Alle UI-Komponenten im Namespace "home" abrufen
namespace = "home"
uiComponents = uiApi.getUiComponents(namespace)
print("Alle UI-Komponenten:\n")
print(uiComponents)

# Eine neue UI-Komponente hinzufügen
componentData = {
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
newComponent = uiApi.addUiComponent(namespace, componentData)
print("Neue UI-Komponente:\n")
print(newComponent)

# Eine spezifische UI-Komponente abrufen
componentUid = "unique-button-uid"
component = uiApi.getUiComponent(namespace, componentUid)
print("Einzelne UI-Komponente:\n")
print(component)

# Eine UI-Komponente aktualisieren
updatedComponentData = {
    "component": "Button",
    "config": {
        "label": "Turn Off Light",
        "action": "turn_off"
    },
    "uid": "unique-button-uid"
}
updatedComponent = uiApi.updateUiComponent(namespace, componentUid, updatedComponentData)
print("Geänderte UI-Komponente:\n")
print(updatedComponent)

# Eine UI-Komponente löschen
deletedComponent = uiApi.deleteUiComponent(namespace, componentUid)
print("Gelöschte UI-Komponente:\n")
print(deletedComponent)

# Alle UI-Kacheln abrufen
uiTiles = uiApi.getUiTiles()
print("Kacheln einer UI-Komponente:\n")
print(uiTiles)
