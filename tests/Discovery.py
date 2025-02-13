import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Discovery

# Test fetching all discovery bindings
def testGetAllDiscoveryBindings(discoveryAPI: Discovery):
    print("\n~~~~ Test #1: getAllDiscoveryBindings() ~~~~\n")

    try:
        response = discoveryAPI.getAllDiscoveryBindings()
        print("Bindings supporting discovery:", response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test starting a discovery scan for a specific binding
def testStartBindingScan(discoveryAPI: Discovery, bindingID: str):
    print("\n~~~~ Test #2: startBindingScan() ~~~~\n")

    try:
        timeout = discoveryAPI.startBindingScan(bindingID=bindingID)
        print(f"Discovery started. Timeout: {timeout} seconds")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    discoveryAPI = Discovery(client)

    # Define test variables
    bindingID = "network"

    # Run all tests
    testGetAllDiscoveryBindings(discoveryAPI)        # Test #1
    testStartBindingScan(discoveryAPI, bindingID)    # Test #2
