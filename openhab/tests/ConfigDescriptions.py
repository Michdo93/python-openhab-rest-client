import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ConfigDescriptions

class ConfigDescriptionsTest:
    def __init__(self, client: OpenHABClient):
        self.configDescriptionsAPI = ConfigDescriptions(client)

    # Test fetching all configuration descriptions
    def testGetConfigDescriptions(self, scheme: str = None, language: str = None):
        print("\n~~~~ Test #1: getConfigDescriptions() ~~~~\n")

        try:
            response = self.configDescriptionsAPI.getConfigDescriptions(language=language, scheme=scheme)
            print("All Configuration Descriptions:", response)
        except Exception as e:
            print(f"Error executing action: {e}")

    # Test fetching a specific configuration description by URI
    def testGetConfigDescription(self, uri: str, language: str = None):
        print("\n~~~~ Test #2: getConfigDescription(uri) ~~~~\n")

        try:
            response = self.configDescriptionsAPI.getConfigDescription(uri=uri, language=language)
            print(f"Configuration Description for URI '{uri}':", response)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
