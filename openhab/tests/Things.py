import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Things

class ThingsTest:
    def __init__(self, client: OpenHABClient):
        self.thingsAPI = Things(client)

    def testGetThings(self, summary: bool = False, staticDataOnly: bool = False, language: str = None):
        """Retrieve all Things"""
        print("\n~~~~ Test #1 getThings() ~~~~\n")

        try:
            allThings = self.thingsAPI.getThings(summary, staticDataOnly, language)
            print(json.dumps(allThings, indent=4))
        except Exception as e:
            print(f"Error retrieving all Things: {e}")

    def testGetThing(self, thingUID: str, language: str = None):
        """Retrieve details for a specific Thing"""
        print("\n~~~~ Test #2 getThing(thingUID) ~~~~\n")

        try:
            thing = self.thingsAPI.getThing(thingUID, language)
            print(json.dumps(thing, indent=4))
        except Exception as e:
            print(f"Error retrieving Thing {thingUID}: {e}")

    def testCreateThing(self, thingData: dict, language: str = None):
        """Create a new Thing"""
        print("\n~~~~ Test #3 createThing(thingData) ~~~~\n")

        try:
            response = self.thingsAPI.createThing(thingData, language)
            print("Thing created:", json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error creating Thing: {e}")

    def testUpdateThing(self, thingUID: str, thingData: dict, language: str = None):
        """Update a Thing"""
        print("\n~~~~ Test #4 updateThing(thingUID, updatedData) ~~~~\n")

        try:
            self.thingsAPI.updateThing(thingUID, thingData, language)
            print(f"Thing {thingUID} updated successfully.")
        except Exception as e:
            print(f"Error updating Thing {thingUID}: {e}")

    def testDeleteThing(self, thingUID: str, force: bool = False, language: str = None):
        """Delete a Thing"""
        print("\n~~~~ Test #5 deleteThing(thingUID) ~~~~\n")
        try:
            self.thingsAPI.deleteThing(thingUID, force, language)
            print(f"Thing {thingUID} deleted successfully.")
        except Exception as e:
            print(f"Error deleting Thing {thingUID}: {e}")

    def testGetThingStatus(self, thingUID: str, language: str = None):
        """Retrieve the status of a Thing"""
        print("\n~~~~ Test #6 getThingStatus(thingUID) ~~~~\n")

        try:
            status = self.thingsAPI.getThingStatus(thingUID, language)
            print(f"Status of Thing {thingUID}: {status}")
        except Exception as e:
            print(f"Error fetching status of Thing {thingUID}: {e}")

    def testSetThingStatus(self, thingUID: str, enabled: bool, language: str = None):
        """Enable or disable a Thing"""
        print("\n~~~~ Test #7 setThingStatus(thingUID, enabled) ~~~~\n")

        try:
            response = self.thingsAPI.setThingStatus(thingUID, enabled, language)
            print(f"Thing {thingUID} enabled: {response}")
        except Exception as e:
            print(f"Error enabling/disabling Thing {thingUID}: {e}")
