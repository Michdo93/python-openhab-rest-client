import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ThingTypes

def testGetAllThingTypes(thingTypesAPI: ThingTypes):
    """Retrieve all thing types"""
    print("\n~~~~ Test #1 getAllThingTypes() ~~~~\n")

    try:
        allThingTypes = thingTypesAPI.getAllThingTypes()
        print("All Thing Types:")
        print(json.dumps(allThingTypes, indent=4))
    except Exception as e:
        print(f"Error retrieving thing types: {e}")

def testGetThingType(thingTypesAPI: ThingTypes, thingTypeUID: str):
    """Retrieve a specific thing type by UID"""
    print("\n~~~~ Test #2 getThingType(thingTypeUID) ~~~~\n")

    try:
        specificThingType = thingTypesAPI.getThingType(thingTypeUID)
        print("Thing Type Details:")
        print(json.dumps(specificThingType, indent=4))
    except Exception as e:
        print(f"Error retrieving thing type {thingTypeUID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingTypesAPI = ThingTypes(client)

    # Example thing type UID
    thingTypeUID = "mqtt:homeassistant"

    # Execute test functions
    testGetAllThingTypes(thingTypesAPI)       # Test #1
    testGetThingType(thingTypesAPI, thingTypeUID)  # Test #2
