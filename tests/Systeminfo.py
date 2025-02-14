import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Systeminfo

def testGetSystemInfo(systemInfoAPI: Systeminfo):
    """Retrieve system information"""
    print("\n~~~~ Test #1 getSystemInfo() ~~~~\n")

    try:
        systemInfo = systemInfoAPI.getSystemInfo()
        print(json.dumps(systemInfo, indent=4))
    except Exception as e:
        print(f"Error retrieving system information: {e}")

def testGetUoMInfo(systemInfoAPI: Systeminfo):
    """Retrieve unit of measurement (UoM) information"""
    print("\n~~~~ Test #2 getUomInfo() ~~~~\n")

    try:
        uomInfo = systemInfoAPI.getUoMInfo()
        print(json.dumps(uomInfo, indent=4))
    except Exception as e:
        print(f"Error retrieving UoM information: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    systemInfoAPI = Systeminfo(client)

    # Execute test functions
    testGetSystemInfo(systemInfoAPI)  # Test #1
    testGetUoMInfo(systemInfoAPI)     # Test #2
