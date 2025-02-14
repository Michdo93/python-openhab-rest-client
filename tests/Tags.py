import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Tags

def testGetTags(tagsAPI: Tags):
    """Retrieve all tags"""
    print("\n~~~~ Test #1 getTags() ~~~~\n")

    try:
        allTags = tagsAPI.getTags()
        print(json.dumps(allTags, indent=4))
    except Exception as e:
        print(f"Error retrieving tags: {e}")

def testCreateTag(tagsAPI: Tags, tagData: dict):
    """Create a new tag"""
    print("\n~~~~ Test #2 createTag(tagData) ~~~~\n")

    try:
        response = tagsAPI.createTag(tagData)
        print("Tag created:", json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error creating tag: {e}")

def testGetTag(tagsAPI: Tags, tagID: str):
    """Retrieve details for a specific tag"""
    print("\n~~~~ Test #3 getTag(tagID) ~~~~\n")

    try:
        tagDetails = tagsAPI.getTag(tagID)
        print(json.dumps(tagDetails, indent=4))
    except Exception as e:
        print(f"Error retrieving tag {tagID}: {e}")

def testUpdateTag(tagsAPI: Tags, tagID: str, updatedTagData: dict):
    """Update a tag"""
    print("\n~~~~ Test #4 updateTag(tagID) ~~~~\n")

    try:
        tagsAPI.updateTag(tagID, updatedTagData)
        print(f"Tag {tagID} updated successfully.")
    except Exception as e:
        print(f"Error updating tag {tagID}: {e}")

def testDeleteTag(tagsAPI: Tags, tagID: str):
    """Delete a tag"""
    print("\n~~~~ Test #5 deleteTag(tagID) ~~~~\n")

    try:
        tagsAPI.deleteTag(tagID)
        print(f"Tag {tagID} deleted successfully.")
    except Exception as e:
        print(f"Error deleting tag {tagID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    tagsAPI = Tags(client)

    # Example tag data
    newTagData = {
        "uid": "CustomTag",
        "name": "CustomTag",
        "label": "My Custom Tag",
        "description": "This is a custom tag",
        "synonyms": ["Custom", "Tag"],
        "editable": True
    }

    # Example tag ID
    tagID = "Property_Voltage"

    # Execute test functions
    testGetTags(tagsAPI)                                                    # Test #1
    testCreateTag(tagsAPI, newTagData)                                      # Test #2
    testGetTag(tagsAPI, tagID)                                              # Test #3
    testUpdateTag(tagsAPI, tagID, {"id": tagID, "label": "Updated Tag"})    # Test #4
    testDeleteTag(tagsAPI, tagID)                                           # Test #5
