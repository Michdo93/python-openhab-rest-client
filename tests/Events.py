import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Events

# Test retrieving all events
def testGetAllEvents(eventsAPI: Events, topics: str = None):
    print("\n~~~~ Test #1: getAllEvents() ~~~~\n")

    try:
        events = eventsAPI.getAllEvents(topics)
        print("(Filtered) Events:", events)
    except ValueError as e:
        print("Error trying to retrieve Events:", e)

# Test initiating new state tracker connection
def testInitiateStateTracker(eventsAPI: Events):
    print("\n~~~~ Test #2: initiateStateTracker() ~~~~\n")

    try:
        connectionIDResponse = eventsAPI.initiateStateTracker()
        print("New Connection ID:", connectionIDResponse)
    except Exception as e:
        print("Error starting the state tracker connection:", e)

    connectionID = None
    for line in connectionIDResponse.iter_lines():
        if line.startswith(b"data: "):  # search line with ID
            connectionID = line.decode().split("data: ")[1].strip()
            break  # Read the first line (data)

    print("Found Connection ID:", connectionID)
    return connectionID

# Test updating connection
def testUpdateSSEConnectionItems(eventsAPI: Events, connectionID: str, items: list):
    print("\n~~~~ Test #3: updateSSEConnectionItems(connectionID, items) ~~~~\n")

    try:
        result = eventsAPI.updateSSEConnectionItems(connectionID=connectionID, items=items)
        print(result)
    except ValueError as e:
        print("Error updating the connection:", e)

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    eventsAPI = Events(client)

    # Variables
    topics = "topic1,topic2"
    items = ["item1", "item2"]

    # Run all tests
    testGetAllEvents(eventsAPI)                                  # Test #1
    testGetAllEvents(eventsAPI, topics)                          # Test #1b
    connectionID = testInitiateStateTracker(eventsAPI)           # Test #2
    testUpdateSSEConnectionItems(eventsAPI, connectionID, items) # Test #3
