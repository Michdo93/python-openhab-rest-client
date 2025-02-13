import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, LinkEvents

def testItemChannelLinkAddedEvent(linkEvents: LinkEvents, itemName: str, channelUID: str):
    """ Test the ItemChannelLinkAddedEvent method """
    print("\n~~~~ Test #1: ItemChannelLinkAddedEvent() ~~~~\n")
    
    try:
        response = linkEvents.ItemChannelLinkAddedEvent(itemName, channelUID)
        print(f"ItemChannelLinkAddedEvent response: {response}")
    except Exception as e:
        print(f"Error in ItemChannelLinkAddedEvent: {e}")

def testItemChannelLinkRemovedEvent(linkEvents: LinkEvents, itemName: str, channelUID: str):
    """ Test the ItemChannelLinkRemovedEvent method """
    print("\n~~~~ Test #2: ItemChannelLinkRemovedEvent() ~~~~\n")
    
    try:
        response = linkEvents.ItemChannelLinkRemovedEvent(itemName, channelUID)
        print(f"ItemChannelLinkRemovedEvent response: {response}")
    except Exception as e:
        print(f"Error in ItemChannelLinkRemovedEvent: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    linkEvents = LinkEvents(client)

    # Test variables
    itemName = "*"
    channelUID = "*"

    # Run tests
    testItemChannelLinkAddedEvent(linkEvents, itemName, channelUID)     # Test#1
    testItemChannelLinkRemovedEvent(linkEvents, itemName, channelUID)   # Test#2
