import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, UUID

# Retrieve the UUID
def testGetUuid(uuidAPI: UUID):
    """Test retrieving the OpenHAB UUID"""
    print("\n~~~~ Test #1: getUUID() ~~~~\n")

    try:
        openhabUUID = uuidAPI.getUUID()
        print(f"The OpenHAB UUID is: {openhabUUID}")
    except Exception as e:
        print(f"Error fetching UUID: {e}")

# Run the test function
if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    uuidAPI = UUID(client)
    
    # Run all tests
    testGetUuid(uuidAPI)    # Test #1
