import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelTypes

# Test fetching all available channel types
def testGetAllChannelTypes(channelTypesAPI: ChannelTypes, language: str = None, prefixes: str = None):
    print("\n~~~~ Test #1: getAllChannelTypes() ~~~~\n")

    try:
        response = channelTypesAPI.getAllChannelTypes(language, prefixes)
        print("Available Channel Types:")
        for channel in response:
            print(channel.get("UID", "No UID found"))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test fetching details of a specific channel type by UID
def testGetChannelTypeByUID(channelTypesAPI: ChannelTypes, channelTypeUID: str, language: str = None):
    print("\n~~~~ Test #2: getChannelTypeByUID() ~~~~\n")

    try:
        response = channelTypesAPI.getChannelTypeByUID(channelTypeUID=channelTypeUID, language=language)
        print("Channel Type Details:", response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test fetching linkable item types for a given channel type
def testGetLinkableItemTypes(channelTypesAPI: ChannelTypes, channelTypeUID: str):
    print("\n~~~~ Test #3: getLinkableItemTypes() ~~~~\n")

    try:
        response = channelTypesAPI.getLinkableItemTypes(channelTypeUID=channelTypeUID)
        print("Linkable Item Types:", response)
    except Exception as e:
        print(f"Error executing action: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    channelTypesAPI = ChannelTypes(client)

    # Define test variables
    language = "en"
    prefix = "mqtt"
    channelTypeUID = "mqtt:trigger"

    # Run all tests
    testGetAllChannelTypes(channelTypesAPI, language)                   # Test #1
    testGetAllChannelTypes(channelTypesAPI, language, prefix)           # Test #1b
    testGetChannelTypeByUID(channelTypesAPI, channelTypeUID, language)  # Test #2
    testGetLinkableItemTypes(channelTypesAPI, channelTypeUID)           # Test #3
