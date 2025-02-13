import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, ConfigDescriptions

# Test fetching all configuration descriptions
def testGetAllConfigDescriptions(configDescriptionsAPI: ConfigDescriptions, language: str = None, scheme: str = None):
    print("\n~~~~ Test #1: getAllConfigDescriptions() ~~~~\n")

    try:
        response = configDescriptionsAPI.getAllConfigDescriptions(language=language, scheme=scheme)
        print("All Configuration Descriptions:", response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test fetching a specific configuration description by URI
def testGetConfigDescriptionByUri(configDescriptionsAPI: ConfigDescriptions, uri: str, language: str = None):
    print("\n~~~~ Test #2: getConfigDescriptionByUri() ~~~~\n")

    try:
        response = configDescriptionsAPI.getConfigDescriptionByUri(uri=uri, language=language)
        print(f"Configuration Description for URI '{uri}':", response)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    configDescriptionsAPI = ConfigDescriptions(client)

    # Define test variables
    language = "en"
    configUri = "channel-type:mqtt:ha-channel"

    # Run all tests
    testGetAllConfigDescriptions(configDescriptionsAPI, language)               # Test #1
    testGetConfigDescriptionByUri(configDescriptionsAPI, configUri, language)   # Test #2
