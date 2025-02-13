import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, InboxEvents

def testInboxAddedEvent(inboxEvents: InboxEvents, thingUID: str = "*"):
    print("\n~~~~ Test #1: InboxAddedEvent(thingUID) ~~~~\n")

    try:
        response = inboxEvents.InboxAddedEvent(thingUID)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")
def testInboxRemovedEvent(inboxEvents: InboxEvents, thingUID: str = "*"):
    print("\n~~~~ Test #2: InboxRemovedEvent(thingUID) ~~~~\n")

    try:
        response = inboxEvents.InboxRemovedEvent(thingUID)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

def testInboxUpdatedEvent(inboxEvents: InboxEvents, thingUID: str = "*"):
    print("\n~~~~ Test #3: InboxUpdatedEvent(thingUID) ~~~~\n")

    try:
        response = inboxEvents.InboxUpdatedEvent(thingUID)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    inboxEvents = InboxEvents(client)

    thingUID = "*"

    # Run all tests
    testInboxAddedEvent(inboxEvents, thingUID)      # Test #1
    testInboxRemovedEvent(inboxEvents, thingUID)    # Test #2
    testInboxUpdatedEvent(inboxEvents, thingUID)    # Test #3
