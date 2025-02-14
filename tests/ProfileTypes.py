import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ProfileTypes

def testGetProfileTypes(profileTypesAPI: ProfileTypes):
    """ Retrieve all available profile types """
    print("\n~~~~ Test #1 getProfileTypes() ~~~~\n")
    try:
        profile_types = profileTypesAPI.getProfileTypes()
        print(json.dumps(profile_types, indent=4))
    except Exception as e:
        print(f"Error retrieving profile types: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    profileTypesAPI = ProfileTypes(client)

    # Run test
    testGetProfileTypes(profileTypesAPI)    # Test #1
