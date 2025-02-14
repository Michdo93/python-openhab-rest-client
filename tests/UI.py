import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, UI

def testGetUiComponents(uiAPI: UI, namespace: str):
    """Retrieve all UI components for a given namespace"""
    print("\n~~~~ Test #1: getUiComponents(namespace) ~~~~\n")

    try:
        components = uiAPI.getUiComponents(namespace)
        print(json.dumps(components, indent=4))
    except Exception as e:
        print(f"Error retrieving UI components for {namespace}: {e}")

def testAddUiComponent(uiAPI: UI, namespace: str, componentData: dict):
    """Add a new UI component"""
    print("\n~~~~ Test #2: addUiComponent(namespace, componentData) ~~~~\n")

    try:
        newComponent = uiAPI.addUiComponent(namespace, componentData)
        print(f"New UI component added:\n{json.dumps(newComponent, indent=4)}")
    except Exception as e:
        print(f"Error adding new UI component: {e}")

def testGetUiComponent(uiAPI: UI, namespace: str, componentUID: str):
    """Retrieve a specific UI component by UID"""
    print("\n~~~~ Test #3: getUiComponent(namespace, componentUID) ~~~~\n")

    try:
        component = uiAPI.getUiComponent(namespace, componentUID)
        print(json.dumps(component, indent=4))
    except Exception as e:
        print(f"Error retrieving UI component {componentUID}: {e}")

def testUpdateUiComponent(uiAPI: UI, namespace: str, componentUID: str, updatedComponentData: dict):
    """Update a UI component by UID"""
    print("\n~~~~ Test #4: updateUiComponent(namespace, componentUID) ~~~~\n")

    try:
        updatedComponent = uiAPI.updateUiComponent(namespace, componentUID, updatedComponentData)
        print(f"Updated UI component {componentUID}:\n{json.dumps(updatedComponent, indent=4)}")
    except Exception as e:
        print(f"Error updating UI component {componentUID}: {e}")

def testDeleteUiComponent(uiAPI: UI, namespace: str, componentUID: str):
    """Delete a UI component by UID"""
    print("\n~~~~ Test #5: deleteUiComponent(namespace, componentUID) ~~~~\n")

    try:
        uiAPI.deleteUiComponent(namespace, componentUID)
        print(f"UI component {componentUID} deleted successfully.")
    except Exception as e:
        print(f"Error deleting UI component {componentUID}: {e}")

def testGetUiTiles(uiAPI: UI):
    """Retrieve all UI tiles"""
    print("\n~~~~ Test #6: getUiTiles() ~~~~\n")

    try:
        tiles = uiAPI.getUiTiles()
        print(json.dumps(tiles, indent=4))
    except Exception as e:
        print(f"Error retrieving UI tiles: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    uiAPI = UI(client)

    # Example data
    namespace = "home"
    componentUID = "unique-button-uid"

    componentData = {
        "component": "Button",
        "config": {"label": "Turn On Light", "action": "turn_on"},
        "slots": {"slot1": [{"component": "Icon", "config": {"icon": "light"}}]},
        "uid": componentUID,
        "tags": ["button", "light-control"],
        "props": {
            "uri": "/control/light",
            "parameters": [{"name": "light", "label": "Light", "type": "TEXT", "required": True}]
        },
        "timestamp": "2025-01-27T15:37:35.741Z",
        "type": "button"
    }

    updatedComponentData = {
        "component": "Button",
        "config": {"label": "Turn Off Light", "action": "turn_off"},
        "uid": componentUID
    }

    # Execute test functions
    testGetUiComponents(uiAPI, namespace)                                       # Test #1
    testAddUiComponent(uiAPI, namespace, componentData)                         # Test #2
    testGetUiComponent(uiAPI, namespace, componentUID)                          # Test #3
    testUpdateUiComponent(uiAPI, namespace, componentUID, updatedComponentData) # Test #4
    testDeleteUiComponent(uiAPI, namespace, componentUID)                       # Test #5
    testGetUiTiles(uiAPI)                                                       # Test #6
