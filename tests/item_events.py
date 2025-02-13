import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ItemEvents

# Test fetching a generic item event
def testItemEvent(itemEventsAPI: ItemEvents):
    print("\n~~~~ Test #1: ItemEvent() ~~~~\n")

    try:
        response = itemEventsAPI.ItemEvent()
        print(response)
    except Exception as e:
        print(f"Error fetching ItemEvent: {e}")

# Test fetching an item added event
def testItemAddedEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #2: ItemAddedEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemAddedEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemAddedEvent: {e}")

# Test fetching an item removed event
def testItemRemovedEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #3: ItemRemovedEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemRemovedEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemRemovedEvent: {e}")

# Test fetching an item updated event
def testItemUpdatedEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #4: ItemUpdatedEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemUpdatedEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemUpdatedEvent: {e}")

# Test fetching an item command event
def testItemCommandEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #5: ItemCommandEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemCommandEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemCommandEvent: {e}")

# Test fetching an item state event
def testItemStateEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #6: ItemStateEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemStateEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemStateEvent: {e}")

# Test fetching an item state predicted event
def testItemStatePredictedEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #7: ItemStatePredictedEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemStatePredictedEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemStatePredictedEvent: {e}")

# Test fetching an item state changed event
def testItemStateChangedEvent(itemEventsAPI: ItemEvents, itemName: str = "*"):
    print("\n~~~~ Test #8: ItemStateChangedEvent(itemName) ~~~~\n")

    try:
        response = itemEventsAPI.ItemStateChangedEvent(itemName)
        print(response)
    except Exception as e:
        print(f"Error fetching ItemStateChangedEvent: {e}")

# Test fetching a group item state changed event
def testGroupItemStateChangedEvent(itemEventsAPI: ItemEvents, itemName: str = "*", memberName: str = "*"):
    print("\n~~~~ Test #9: GroupItemStateChangedEvent(itemName, memberName) ~~~~\n")

    try:
        response = itemEventsAPI.GroupItemStateChangedEvent(itemName, memberName)
        print(response)
    except Exception as e:
        print(f"Error fetching GroupItemStateChangedEvent: {e}")

# Test processing ItemStateChangedEvent stream
def testItemStateChangedEventStream(itemEventsAPI: ItemEvents):
    print("\n~~~~ Test #10: ItemStateChangedEvent Stream() ~~~~\n")

    try:
        response = itemEventsAPI.ItemStateChangedEvent()
        with response as events:
            for line in events.iter_lines():
                line = line.decode()

                if "data" in line:
                    line = line.replace("data: ", "")
                    try:
                        data = json.loads(line)
                        print(data)
                    except json.decoder.JSONDecodeError:
                        print("Event could not be converted to JSON")
    except Exception as e:
        print(f"Error processing ItemStateChangedEvent stream: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    itemEventsAPI = ItemEvents(client)

    # Variables
    itemName = "*"
    memberName = "*"

    # Run all tests
    testItemEvent(itemEventsAPI)                                            # Test #1
    testItemAddedEvent(itemEventsAPI, itemName)                             # Test #2
    testItemRemovedEvent(itemEventsAPI, itemName)                           # Test #3
    testItemUpdatedEvent(itemEventsAPI, itemName)                           # Test #4
    testItemCommandEvent(itemEventsAPI, itemName)                           # Test #5
    testItemStateEvent(itemEventsAPI, itemName)                             # Test #6
    testItemStatePredictedEvent(itemEventsAPI, itemName)                    # Test #7
    testItemStateChangedEvent(itemEventsAPI, itemName)                      # Test #8
    testGroupItemStateChangedEvent(itemEventsAPI, itemName, memberName)     # Test #9
    testItemStateChangedEventStream(itemEventsAPI)                          # Test #10
