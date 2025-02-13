import sys
import os
import json
import time

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Links

def testGetAllLinks(linksAPI: Links):
    """ Test fetching all links """
    print("\n~~~~ Test #1: getAllLinks() ~~~~\n")

    try:
        allLinks = linksAPI.getAllLinks()
        print(json.dumps(allLinks, indent=2))
    except Exception as e:
        print(f"Error retrieving all links: {e}")

def testGetIndividualLink(linksAPI: Links, itemName: str, channelUID: str):
    """ Test fetching a specific link """
    print(f"\n~~~~ Test #2: getIndividualLink({itemName}, {channelUID}) ~~~~\n")

    try:
        link = linksAPI.getIndividualLink(itemName, channelUID)
        print(json.dumps(link, indent=2))
    except Exception as e:
        print(f"Error retrieving link {itemName} -> {channelUID}: {e}")

def testUnlinkItemFromChannel(linksAPI: Links, itemName: str, channelUID: str):
    """ Test unlinking an item from a channel """
    print(f"\n~~~~ Test #3: unlinkItemFromChannel({itemName}, {channelUID}) ~~~~\n")

    try:
        response = linksAPI.unlinkItemFromChannel(itemName, channelUID)
        print(f"Link removed: {response}")
        time.sleep(1)  # Small delay for API stability
    except Exception as e:
        print(f"Error unlinking {itemName} -> {channelUID}: {e}")

def testLinkItemToChannel(linksAPI: Links, itemName: str, channelUID: str, config: dict = {}):
    """ Test linking an item to a channel """
    print(f"\n~~~~ Test #4: linkItemToChannel({itemName}, {channelUID}) ~~~~\n")

    try:
        response = linksAPI.linkItemToChannel(itemName, channelUID, config)
        print(f"Link created: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"Error linking {itemName} -> {channelUID}: {e}")

def testGetOrphanLinks(linksAPI: Links):
    """ Test retrieving orphan links """
    print("\n~~~~ Test #5: getOrphanLinks() ~~~~\n")

    try:
        orphanLinks = linksAPI.getOrphanLinks()
        print(json.dumps(orphanLinks, indent=2))
    except Exception as e:
        print(f"Error retrieving orphan links: {e}")

def testPurgeUnusedLinks(linksAPI: Links):
    """ Test purging unused links """
    print("\n~~~~ Test #6: purgeUnusedLinks() ~~~~\n")

    try:
        response = linksAPI.purgeUnusedLinks()
        print(f"Unused links purged: {response}")
    except Exception as e:
        print(f"Error purging unused links: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    linksAPI = Links(client)

    # Test variables
    itemName = "Sunrise_Time"
    channelUID = "astro:sun:b54938fe5crise#start"

    # Run tests
    testGetAllLinks(linksAPI)                                   # Test#1
    testGetIndividualLink(linksAPI, itemName, channelUID)       # Test#2
    testUnlinkItemFromChannel(linksAPI, itemName, channelUID)   # Test#3
    testLinkItemToChannel(linksAPI, itemName, channelUID)       # Test#4
    testGetOrphanLinks(linksAPI)                                # Test#5
    testPurgeUnusedLinks(linksAPI)                              # Test#6
