import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Discovery

class DiscoveryTest:
    def __init__(self, client: OpenHABClient):
        self.discoveryAPI = Discovery(client)

    # Test fetching all discovery bindings
    def testGetDiscoveryBindings(self):
        print("\n~~~~ Test #1: getDiscoveryBindings() ~~~~\n")

        try:
            response = self.discoveryAPI.getDiscoveryBindings()
            print("Bindings supporting discovery:", response)
        except Exception as e:
            print(f"Error executing action: {e}")

    def testGetBindingInfo(self, bindingID: str, language: str = None):
        print("\n~~~~ Test #1: getDiscoveryBindings(bindingID) ~~~~\n")

        try:
            response = self.discoveryAPI.getBindingInfo(bindingID, language)
            print("Binding info:", response)
        except Exception as e:
            print(f"Error executing action: {e}")
            
    # Test starting a discovery scan for a specific binding
    def testStartBindingScan(self, bindingID: str, input: str = None):
        print("\n~~~~ Test #2: startBindingScan(bindingID) ~~~~\n")

        try:
            timeout = self.discoveryAPI.startBindingScan(bindingID, input)
            print(f"Discovery started. Timeout: {timeout} seconds")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
