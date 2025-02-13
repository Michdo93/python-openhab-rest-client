import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Items

# Test fetching all items
def testGetAllItems(itemsAPI: Items):
    print("\n~~~~ Test #1: getAllItems() ~~~~\n")

    try:
        allItems = itemsAPI.getAllItems()
        print("All Items:", allItems)
    except Exception as e:
        print(f"Error fetching all items: {e}")

# Test fetching a specific item
def testGetItem(itemsAPI: Items, itemName: str):
    print("\n~~~~ Test #2: getItem() ~~~~\n")

    try:
        item = itemsAPI.getItem(itemName)
        print(f"Details for {itemName}:", item)
    except Exception as e:
        print(f"Error fetching item '{itemName}': {e}")

# Test adding or updating a single item
def testAddOrUpdateItem(itemsAPI: Items, itemName: str, itemData: dict):
    print("\n~~~~ Test #3: addOrUpdateItem() ~~~~\n")

    try:
        itemsAPI.addOrUpdateItem(itemName, itemData)
        print(f"Item '{itemName}' added or updated.")
    except Exception as e:
        print(f"Error adding or updating item '{itemName}': {e}")

# Test adding or updating multiple items
def testAddOrUpdateItems(itemsAPI: Items, items: list):
    print("\n~~~~ Test #4: addOrUpdateItems() ~~~~\n")

    try:
        itemsAPI.addOrUpdateItems(items)
        print("Multiple items added or updated.")
    except Exception as e:
        print(f"Error adding or updating multiple items: {e}")

# Test sending a command to an item
def testSendCommand(itemsAPI: Items, itemName: str, command: str):
    print("\n~~~~ Test #5: sendCommand() ~~~~\n")

    try:
        itemsAPI.sendCommand(itemName, command)
        print(f"Command '{command}' sent to '{itemName}'.")
    except Exception as e:
        print(f"Error sending command to '{itemName}': {e}")

# Test updating the state of an item
def testUpdateItemState(itemsAPI: Items, itemName: str, state: str):
    print("\n~~~~ Test #6: updateItemState() ~~~~\n")

    try:
        itemsAPI.updateItemState(itemName, state)
        print(f"State of '{itemName}' updated to '{state}'.")
    except Exception as e:
        print(f"Error updating state of '{itemName}': {e}")

# Test fetching the state of an item
def testGetItemState(itemsAPI: Items, itemName: str):
    print("\n~~~~ Test #7: getItemState() ~~~~\n")

    try:
        state = itemsAPI.getItemState(itemName)
        print(f"State of '{itemName}':", state)
    except Exception as e:
        print(f"Error fetching state of '{itemName}': {e}")

# Test deleting an item
def testDeleteItem(itemsAPI: Items, itemName: str):
    print("\n~~~~ Test #8: deleteItem() ~~~~\n")

    try:
        itemsAPI.deleteItem(itemName)
        print(f"Item '{itemName}' deleted.")
    except Exception as e:
        print(f"Error deleting item '{itemName}': {e}")

# Test adding a group member
def testAddGroupMember(itemsAPI: Items, groupName: str, itemName: str):
    print("\n~~~~ Test #9: addGroupMember() ~~~~\n")

    try:
        itemsAPI.addGroupMember(groupName, itemName)
        print(f"Item '{itemName}' added to group '{groupName}'.")
    except Exception as e:
        print(f"Error adding item '{itemName}' to group '{groupName}': {e}")

# Test removing a group member
def testRemoveGroupMember(itemsAPI: Items, groupName: str, itemName: str):
    print("\n~~~~ Test #10: removeGroupMember() ~~~~\n")

    try:
        itemsAPI.removeGroupMember(groupName, itemName)
        print(f"Item '{itemName}' removed from group '{groupName}'.")
    except Exception as e:
        print(f"Error removing item '{itemName}' from group '{groupName}': {e}")

# Test adding metadata to an item
def testAddMetadata(itemsAPI: Items, itemName: str, namespace: str, metadata: dict):
    print("\n~~~~ Test #11: addMetadata() ~~~~\n")

    try:
        itemsAPI.addMetadata(itemName, namespace, metadata)
        print(f"Metadata added to '{itemName}' in namespace '{namespace}'.")
    except Exception as e:
        print(f"Error adding metadata to '{itemName}': {e}")

# Test removing metadata from an item
def testRemoveMetadata(itemsAPI: Items, itemName: str, namespace: str):
    print("\n~~~~ Test #12: removeMetadata() ~~~~\n")

    try:
        itemsAPI.removeMetadata(itemName, namespace)
        print(f"Metadata removed from '{itemName}' in namespace '{namespace}'.")
    except Exception as e:
        print(f"Error removing metadata from '{itemName}': {e}")

# Test fetching metadata namespaces of an item
def testGetMetadataNamespaces(itemsAPI: Items, itemName: str):
    print("\n~~~~ Test #13: getMetadataNamespaces() ~~~~\n")

    try:
        namespaces = itemsAPI.getMetadataNamespaces(itemName)
        print(f"Metadata namespaces for '{itemName}':", namespaces)
    except Exception as e:
        print(f"Error fetching metadata namespaces for '{itemName}': {e}")

# Test purging orphaned metadata
def testPurgeOrphanedMetadata(itemsAPI: Items):
    print("\n~~~~ Test #14: purgeOrphanedMetadata() ~~~~\n")

    try:
        itemsAPI.purgeOrphanedMetadata()
        print("Orphaned metadata purged.")
    except Exception as e:
        print(f"Error purging orphaned metadata: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    itemsAPI = Items(client)

    # Define test variables
    testItemName = "testSwitch"
    newItemData = {
        "type": "Switch",
        "name": "newSwitch",
        "label": "New Switch",
        "groupNames": ["Static"],
        "tags": ["SwitchTag"],
        "category": "Switch"
    }
    testMetadata = {
        "value": "metadata_value",
        "config": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    
    # Run tests
    testGetAllItems(itemsAPI)                                                   # Test#1
    testGetItem(itemsAPI, testItemName)                                         # Test#2
    testAddOrUpdateItem(itemsAPI, "newSwitch", newItemData)                     # Test#3
    testAddOrUpdateItems(itemsAPI, [newItemData])                               # Test#4
    testSendCommand(itemsAPI, testItemName, "ON")                               # Test#5
    testUpdateItemState(itemsAPI, "testNumber", "42")                           # Test#6
    testGetItemState(itemsAPI, testItemName)                                    # Test#7
    testDeleteItem(itemsAPI, "newSwitch")                                       # Test#8
    testAddGroupMember(itemsAPI, "Static", "testNumber")                        # Test#9
    testRemoveGroupMember(itemsAPI, "Static", "testNumber")                     # Test#10
    testAddMetadata(itemsAPI, testItemName, "exampleNamespace", testMetadata)   # Test#11
    testRemoveMetadata(itemsAPI, testItemName, "exampleNamespace")              # Test#12
    testGetMetadataNamespaces(itemsAPI, testItemName)                           # Test#13
    testPurgeOrphanedMetadata(itemsAPI)                                         # Test#14
