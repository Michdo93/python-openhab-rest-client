import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Services

def testGetAllServices(servicesAPI: Services, language: str = "de"):
    """Retrieve all services"""
    print("\n~~~~ Test #1 getServices() ~~~~\n")

    try:
        services = servicesAPI.getServices(language=language)
        print(json.dumps(services, indent=4))
    except Exception as e:
        print(f"Error retrieving services: {e}")

def testGetService(servicesAPI: Services, serviceID: str):
    """Retrieve a specific service"""
    print("\n~~~~ Test #2 getService(serviceID) ~~~~\n")

    try:
        service = servicesAPI.getService(serviceID)
        print(json.dumps(service, indent=4))
    except Exception as e:
        print(f"Error retrieving service {serviceID}: {e}")

def testGetServiceConfig(servicesAPI: Services, serviceID: str):
    """Retrieve the configuration of a service"""
    print("\n~~~~ Test #3 getServiceConfig(serviceID) ~~~~\n")

    try:
        config = servicesAPI.getServiceConfig(serviceID)
        print(json.dumps(config, indent=4))
    except Exception as e:
        print(f"Error retrieving configuration for {serviceID}: {e}")

def testUpdateServiceConfig(servicesAPI: Services, serviceID: str, newConfig: dict):
    """Update the configuration of a service"""
    print("\n~~~~ Test #4 updateServiceConfig(serviceID) ~~~~\n")

    try:
        old_config = servicesAPI.updateServiceConfig(serviceID, newConfig)
        print("Old Configuration:", json.dumps(old_config, indent=4))
    except Exception as e:
        print(f"Error updating configuration for {serviceID}: {e}")

def testDeleteServiceConfig(servicesAPI: Services, serviceID: str):
    """Delete the configuration of a service"""
    print("\n~~~~ Test #5 deleteServiceConfig(serviceID) ~~~~\n")

    try:
        deleted_config = servicesAPI.deleteServiceConfig(serviceID)
        print("Deleted Configuration:", json.dumps(deleted_config, indent=4))
    except Exception as e:
        print(f"Error deleting configuration for {serviceID}: {e}")

def testGetServiceContexts(servicesAPI: Services, serviceID: str):
    """Retrieve all contexts of a service"""
    print("\n~~~~ Test #6 getServiceContexts(serviceID) ~~~~\n")

    try:
        contexts = servicesAPI.getServiceContexts(serviceID)
        print(json.dumps(contexts, indent=4))
    except Exception as e:
        print(f"Error retrieving contexts for {serviceID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    servicesAPI = Services(client)

    # Example service ID
    serviceID = "org.openhab.i18n"
    
    # Example new configuration
    newConfig = {
        "enabled": True,
        "setting1": "newValue1"
    }

    # Execute test functions
    testGetAllServices(servicesAPI)                             # Test #1
    testGetService(servicesAPI, serviceID)                      # Test #2
    testGetServiceConfig(servicesAPI, serviceID)                # Test #3
    testUpdateServiceConfig(servicesAPI, serviceID, newConfig)  # Test #4
    testDeleteServiceConfig(servicesAPI, serviceID)             # Test #5
    testGetServiceContexts(servicesAPI, serviceID)              # Test #6
