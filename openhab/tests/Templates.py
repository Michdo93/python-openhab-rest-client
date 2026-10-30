import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Templates

class TemplatesTest:
    def __init__(self, client: OpenHABClient):
        self.templatesAPI = Templates(client)

    def testGetTemplates(self, language: str = None):
        """Retrieve all templates"""
        print("\n~~~~ Test #1 getTemplates() ~~~~\n")

        try:
            allTemplates = self.templatesAPI.getAllTemplates(language)
            print("All Templates:")
            print(json.dumps(allTemplates, indent=4))
        except Exception as e:
            print(f"Error retrieving templates: {e}")

    def testGetTemplate(self, templateUID: str, language: str = None):
        """Retrieve a specific template by UID"""
        print("\n~~~~ Test #2 getTemplate(templateUID) ~~~~\n")

        try:
            specificTemplate = self.templatesAPI.getTemplate(templateUID, language)
            print("Template Details:")
            print(json.dumps(specificTemplate, indent=4))
        except Exception as e:
            print(f"Error retrieving template {templateUID}: {e}")
