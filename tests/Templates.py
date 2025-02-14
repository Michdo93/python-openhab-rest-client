import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Templates

def testGetAllTemplates(templatesAPI: Templates):
    """Retrieve all templates"""
    print("\n~~~~ Test #1 getAllTemplates() ~~~~\n")

    try:
        allTemplates = templatesAPI.getAllTemplates()
        print("All Templates:")
        print(json.dumps(allTemplates, indent=4))
    except Exception as e:
        print(f"Error retrieving templates: {e}")

def testGetTemplateByUID(templatesAPI: Templates, templateUID: str):
    """Retrieve a specific template by UID"""
    print("\n~~~~ Test #2 getTemplateByUid(templateUID) ~~~~\n")

    try:
        specificTemplate = templatesAPI.getTemplateByUID(templateUID)
        print("Template Details:")
        print(json.dumps(specificTemplate, indent=4))
    except Exception as e:
        print(f"Error retrieving template {templateUID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    templatesAPI = Templates(client)

    # Example template UID
    templateUID = "example_template_uid"

    # Execute test functions
    testGetAllTemplates(templatesAPI)       # Test #1
    testGetTemplateByUID(templatesAPI, templateUID)  # Test #2
