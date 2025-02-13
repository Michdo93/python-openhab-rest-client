import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Inbox

# Test fetching all discovered things
def testGetAllDiscoveredThings(inboxAPI: Inbox, includeIgnored: bool = True):
    print("\n~~~~ Test #1: getAllDiscoveredThings() ~~~~\n")

    try:
        response = inboxAPI.getAllDiscoveredThings(includeIgnored)
        print("Discovered Things:", response)
    except Exception as e:
        print(f"Error retrieving discovered things: {e}")

# Test removing a discovery result
def testRemoveDiscoveryResult(inboxAPI: Inbox, thingUID: str):
    print("\n~~~~ Test #2: removeDiscoveryResult(thingUID) ~~~~\n")

    try:
        response = inboxAPI.removeDiscoveryResult(thingUID)
        print(f"Discovery result '{thingUID}' removed:", response)
    except Exception as e:
        print(f"Error removing discovery result '{thingUID}': {e}")

# Test approving a discovered thing
def testApproveDiscoveryResult(inboxAPI: Inbox, thingUID: str, thingLabel: str, newThingID: str = None, language: str = None):
    print("\n~~~~ Test #3: approveDiscoveryResult(thingUID, thingLabel) ~~~~\n")

    try:
        response = inboxAPI.approveDiscoveryResult(thingUID, thingLabel, newThingID, language)
        print(f"Discovery result '{thingUID}' approved:", response)
    except Exception as e:
        print(f"Error approving discovery result '{thingUID}': {e}")

# Test ignoring a discovery result
def testIgnoreDiscoveryResult(inboxAPI: Inbox, thingUID: str):
    print("\n~~~~ Test #4: ignoreDiscoveryResult(thingUID) ~~~~\n")

    try:
        response = inboxAPI.ignoreDiscoveryResult(thingUID)
        print(f"Discovery result '{thingUID}' ignored:", response)
    except Exception as e:
        print(f"Error ignoring discovery result '{thingUID}': {e}")

# Test unignoring a discovery result
def testUnignoreDiscoveryResult(inboxAPI: Inbox, thingUID: str):
    print("\n~~~~ Test #5: unignoreDiscoveryResult(thingUID) ~~~~\n")

    try:
        response = inboxAPI.unignoreDiscoveryResult(thingUID)
        print(f"Discovery result '{thingUID}' unignored:", response)
    except Exception as e:
        print(f"Error unignoring discovery result '{thingUID}': {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    inboxAPI = Inbox(client)

    # Define test variables
    thingUIDToRemove = "avmfritz:fritzbox:192_168_3_1"
    thingUIDToApprove = "avmfritz:fritzbox:192_168_2_1"
    thingLabel = "My FritzBox Router"
    thingUIDToIgnore = "avmfritz:fritzbox:192_168_2_1"
    thingUIDToUnignore = "avmfritz:fritzbox:192_168_2_1"

    # Run all tests
    testGetAllDiscoveredThings(inboxAPI)                                # Test #1
    testRemoveDiscoveryResult(inboxAPI, thingUIDToRemove)               # Test #2
    testApproveDiscoveryResult(inboxAPI, thingUIDToApprove, thingLabel) # Test #3
    testIgnoreDiscoveryResult(inboxAPI, thingUIDToIgnore)               # Test #4
    testUnignoreDiscoveryResult(inboxAPI, thingUIDToUnignore)           # Test #5
