import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ThingEvents

def testThingAddedEvent(thingEventsAPI: ThingEvents, thingUID: str):
    """Test fetching ThingAddedEvent"""
    print("\n~~~~ Test #1: ThingAddedEvent(thingUID) ~~~~\n")

    try:
        event = thingEventsAPI.ThingAddedEvent(thingUID)
        print(event)
    except Exception as e:
        print(f"Error fetching ThingAddedEvent: {e}")

def testThingRemovedEvent(thingEventsAPI: ThingEvents, thingUID: str):
    """Test fetching ThingRemovedEvent"""
    print("\n~~~~ Test #2: ThingRemovedEvent(thingUID) ~~~~\n")

    try:
        event = thingEventsAPI.ThingRemovedEvent(thingUID)
        print(event)
    except Exception as e:
        print(f"Error fetching ThingRemovedEvent: {e}")

def testThingUpdatedEvent(thingEventsAPI: ThingEvents, thingUID: str):
    """Test fetching ThingUpdatedEvent"""
    print("\n~~~~ Test #3: ThingUpdatedEvent(thingUID) ~~~~\n")

    try:
        event = thingEventsAPI.ThingUpdatedEvent(thingUID)
        print(event)
    except Exception as e:
        print(f"Error fetching ThingUpdatedEvent: {e}")

def testThingStatusInfoEvent(thingEventsAPI: ThingEvents, thingUID: str):
    """Test fetching ThingStatusInfoEvent"""
    print("\n~~~~ Test #4: ThingStatusInfoEvent(thingUID) ~~~~\n")

    try:
        event = thingEventsAPI.ThingStatusInfoEvent(thingUID)
        print(event)
    except Exception as e:
        print(f"Error fetching ThingStatusInfoEvent: {e}")

def testThingStatusInfoChangedEvent(thingEventsAPI: ThingEvents, thingUID: str):
    """Test fetching ThingStatusInfoChangedEvent"""
    print("\n~~~~ Test #5: ThingStatusInfoChangedEvent(thingUID) ~~~~\n")

    try:
        event = thingEventsAPI.ThingStatusInfoChangedEvent(thingUID)
        print(event)
    except Exception as e:
        print(f"Error fetching ThingStatusInfoChangedEvent: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    thingEventsAPI = ThingEvents(client)

    # Define event filter
    thingUID = "*"

    # Run tests
    testThingAddedEvent(thingEventsAPI, thingUID)                # Test #1
    testThingRemovedEvent(thingEventsAPI, thingUID)              # Test #2
    testThingUpdatedEvent(thingEventsAPI, thingUID)              # Test #3
    testThingStatusInfoEvent(thingEventsAPI, thingUID)           # Test #4
    testThingStatusInfoChangedEvent(thingEventsAPI, thingUID)    # Test #5
