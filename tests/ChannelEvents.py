import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelEvents

# Test the event for channel description change
def testChannelDescriptionChangedEvent(channelEvents: ChannelEvents):
    print("\n~~~~ Test #1: ChannelDescriptionChangedEvent() ~~~~\n")

    try:
        response = channelEvents.ChannelDescriptionChangedEvent("*")
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the event for channel triggered
def testChannelTriggeredEvent(channelEvents: ChannelEvents):
    print("\n~~~~ Test #2: ChannelTriggeredEvent() ~~~~\n")

    try:
        response = channelEvents.ChannelTriggeredEvent("*")
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    channelEvents = ChannelEvents(client)

    # Run all tests
    testChannelDescriptionChangedEvent(channelEvents)   # Test #1
    testChannelTriggeredEvent(channelEvents)            # Test #2
