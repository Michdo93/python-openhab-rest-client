import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Things

def testGetAllThings(thingsAPI: Things):
    """Retrieve all Things"""
    print("\n~~~~ Test #1 getAllThings() ~~~~\n")

    try:
        allThings = thingsAPI.getAllThings()
        print(json.dumps(allThings, indent=4))
    except Exception as e:
        print(f"Error retrieving all Things: {e}")

def testGetThingByUID(thingsAPI: Things, thingUID: str):
    """Retrieve details for a specific Thing"""
    print("\n~~~~ Test #2 getThingByUID(thingUID) ~~~~\n")

    try:
        thing = thingsAPI.getThingByUID(thingUID)
        print(json.dumps(thing, indent=4))
    except Exception as e:
        print(f"Error retrieving Thing {thingUID}: {e}")

def testCreateThing(thingsAPI: Things, newThing: dict):
    """Create a new Thing"""
    print("\n~~~~ Test #3 createThing(newThing) ~~~~\n")

    try:
        response = thingsAPI.createThing(newThing)
        print("Thing created:", json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error creating Thing: {e}")

def testUpdateThing(thingsAPI: Things, thingUID: str, updatedData: dict):
    """Update a Thing"""
    print("\n~~~~ Test #4 updateThing(thingUID, updatedData) ~~~~\n")

    try:
        thingsAPI.updateThing(thingUID, updatedData)
        print(f"Thing {thingUID} updated successfully.")
    except Exception as e:
        print(f"Error updating Thing {thingUID}: {e}")

def testDeleteThing(thingsAPI: Things, thingUID: str):
    """Delete a Thing"""
    print("\n~~~~ Test #5 deleteThing(thingUID) ~~~~\n")
    try:
        thingsAPI.deleteThing(thingUID, force=True)
        print(f"Thing {thingUID} deleted successfully.")
    except Exception as e:
        print(f"Error deleting Thing {thingUID}: {e}")

def testGetThingStatus(thingsAPI: Things, thingUID: str):
    """Retrieve the status of a Thing"""
    print("\n~~~~ Test #6 getThingStatus(thingUID) ~~~~\n")

    try:
        status = thingsAPI.getThingStatus(thingUID)
        print(f"Status of Thing {thingUID}: {status}")
    except Exception as e:
        print(f"Error fetching status of Thing {thingUID}: {e}")

def testEnableThing(thingsAPI: Things, thingUID: str, enabled: bool):
    """Enable or disable a Thing"""
    print("\n~~~~ Test #7 enableThing(thingUID, enabled) ~~~~\n")

    try:
        response = thingsAPI.enableThing(thingUID, enabled)
        print(f"Thing {thingUID} enabled: {response}")
    except Exception as e:
        print(f"Error enabling/disabling Thing {thingUID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingsAPI = Things(client)

    # Example Thing data
    thingUID = "mqtt:topic:mybroker:newthing"
    newThing = {
        "UID": "mqtt:topic:mybroker:newthing",
        "label": "New MQTT Thing",
        "thingTypeUID": "mqtt:topic",
        "bridgeUID": "mqtt:broker:mybroker",
        "configuration": {},
        "channels": []
    }
    updatedData = {"label": "Updated MQTT Thing"}

    # Execute test functions
    testGetAllThings(thingsAPI)                         # Test #1
    testGetThingByUID(thingsAPI, thingUID)              # Test #2
    testCreateThing(thingsAPI, newThing)                # Test #3
    testUpdateThing(thingsAPI, thingUID, updatedData)   # Test #4
    testDeleteThing(thingsAPI, thingUID)                # Test #5
    testGetThingStatus(thingsAPI, thingUID)             # Test #6
    testEnableThing(thingsAPI, thingUID, enabled=True)  # Test #7
