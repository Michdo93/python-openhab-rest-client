import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ChannelTypes

class ChannelTypesTest:
    def __init__(self, client: OpenHABClient):
        self.channelTypesAPI = ChannelTypes(client)

    # Test fetching all available channel types
    def testGetChannelTypes(self, prefixes: str = None, language: str = None):
        print("\n~~~~ Test #1: getChannelTypes() ~~~~\n")

        try:
            response = self.channelTypesAPI.getChannelTypes(prefixes, language)
            print("Available Channel Types:")
            for channel in response:
                print(channel.get("UID", "No UID found"))
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test fetching details of a specific channel type by UID
    def testGetChannelType(self, channelTypeUID: str, language: str = None):
        print("\n~~~~ Test #2: getChannelType(channelTypeUID) ~~~~\n")

        try:
            response = self.channelTypesAPI.getChannelType(channelTypeUID=channelTypeUID, language=language)
            print("Channel Type Details:", response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test fetching linkable item types for a given channel type
    def testGetLinkableItemTypes(self, channelTypeUID: str):
        print("\n~~~~ Test #3: getLinkableItemTypes(channelTypeUID) ~~~~\n")

        try:
            response = self.channelTypesAPI.getLinkableItemTypes(channelTypeUID=channelTypeUID)
            print("Linkable Item Types:", response)
        except Exception as e:
            print(f"Error executing action: {e}")
