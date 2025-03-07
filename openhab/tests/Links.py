import sys
import os
import json
import time

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Links

class LinksTest:
    def __init__(self, client: OpenHABClient):
        self.linksAPI = Links(client)

    def testGetLinks(self, channelUID: str = None, itemName: str = None):
        """ Test fetching all links """
        print("\n~~~~ Test #1: getLinks() ~~~~\n")

        try:
            allLinks = self.linksAPI.getLinks(channelUID, itemName)
            print(json.dumps(allLinks, indent=2))
        except Exception as e:
            print(f"Error retrieving all links: {e}")

    def testGetLink(self, itemName: str, channelUID: str):
        """ Test fetching a specific link """
        print("\n~~~~ Test #2: getLink(itemName, channelUID) ~~~~\n")

        try:
            link = self.linksAPI.getLink(itemName, channelUID)
            print(json.dumps(link, indent=2))
        except Exception as e:
            print(f"Error retrieving link {itemName} -> {channelUID}: {e}")

    def testUnlinkItemFromChannel(self, itemName: str, channelUID: str):
        """ Test unlinking an item from a channel """
        print("\n~~~~ Test #3: unlinkItemFromChannel(itemName, channelUID) ~~~~\n")

        try:
            response = self.linksAPI.unlinkItemFromChannel(itemName, channelUID)
            print(f"Link removed: {response}")
            time.sleep(1)  # Small delay for API stability
        except Exception as e:
            print(f"Error unlinking {itemName} -> {channelUID}: {e}")

    def testLinkItemToChannel(self, itemName: str, channelUID: str, configuration: dict = {}):
        """ Test linking an item to a channel """
        print("\n~~~~ Test #4: linkItemToChannel(itemName, channelUID, configuration) ~~~~\n")

        try:
            response = self.linksAPI.linkItemToChannel(itemName, channelUID, configuration)
            print(f"Link created: {json.dumps(response, indent=2)}")
        except Exception as e:
            print(f"Error linking {itemName} -> {channelUID}: {e}")

    def testDeleteAllLinks(self, object: str):
        """ Test deleting all links """
        print("\n~~~~ Test #5: deleteAllLinks(object) ~~~~\n")

        try:
            orphanLinks = self.linksAPI.deleteAllLinks(object)
            print(json.dumps(orphanLinks, indent=2))
        except Exception as e:
            print(f"Error retrieving orphan links: {e}")

    def testGetOrphanLinks(self):
        """ Test retrieving orphan links """
        print("\n~~~~ Test #6: getOrphanLinks() ~~~~\n")

        try:
            orphanLinks = self.linksAPI.getOrphanLinks()
            print(json.dumps(orphanLinks, indent=2))
        except Exception as e:
            print(f"Error retrieving orphan links: {e}")

    def testPurgeUnusedLinks(self):
        """ Test purging unused links """
        print("\n~~~~ Test #7: purgeUnusedLinks() ~~~~\n")

        try:
            response = self.linksAPI.purgeUnusedLinks()
            print(f"Unused links purged: {response}")
        except Exception as e:
            print(f"Error purging unused links: {e}")
