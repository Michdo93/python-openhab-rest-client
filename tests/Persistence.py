import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Persistence

def testGetAllPersistenceServices(persistenceAPI: Persistence):
    """ Retrieve all available persistence services """
    print("\n~~~~ Test #1: getAllServices() ~~~~\n")

    try:
        services = persistenceAPI.getAllServices()
        print(json.dumps(services, indent=4))
    except Exception as e:
        print(f"Error retrieving persistence services: {e}")

def testGetServiceConfiguration(persistenceAPI: Persistence, serviceID: str):
    """ Retrieve the configuration of a specific persistence service """
    print("\n~~~~ Test #2: getServiceConfiguration(serviceID) ~~~~\n")

    try:
        config = persistenceAPI.getServiceConfiguration(serviceID)
        print(json.dumps(config, indent=4))
    except Exception as e:
        print(f"Error retrieving configuration for {serviceID}: {e}")

def testSetServiceConfiguration(persistenceAPI: Persistence, serviceID: str, newConfig: dict):
    """ Update the configuration of a persistence service """
    print("\n~~~~ Test #3: setServiceConfiguration(serviceID) ~~~~\n")

    try:
        updatedConfig = persistenceAPI.setServiceConfiguration(serviceID, newConfig)
        print(json.dumps(updatedConfig, indent=4))
    except Exception as e:
        print(f"Error updating configuration for {serviceID}: {e}")

def testDeleteServiceConfiguration(persistenceAPI: Persistence, serviceID: str):
    """ Delete the configuration of a persistence service """
    print("\n~~~~ Test #4: deleteServiceConfiguration(serviceID) ~~~~\n")

    try:
        response = persistenceAPI.deleteServiceConfiguration(serviceID)
        print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error deleting configuration for {serviceID}: {e}")

def testGetItemsForService(persistenceAPI: Persistence, serviceID: str):
    """ Retrieve all items stored by a specific persistence service """
    print("\n~~~~ Test #5: getItemsForService(serviceID) ~~~~\n")

    try:
        items = persistenceAPI.getItemsForService(serviceID)
        print(json.dumps(items, indent=4))
    except Exception as e:
        print(f"Error retrieving items for service {serviceID}: {e}")

def testGetItemPersistenceData(persistenceAPI: Persistence, serviceID: str, itemName: str, startTime: str, endTime: str):
    """ Retrieve persistence data for a specific item """
    print("\n~~~~ Test #6: getItemPersistenceData(itemName) ~~~~\n")

    try:
        itemData = persistenceAPI.getItemPersistenceData(serviceID, itemName, startTime=startTime, endTime=endTime)
        print(json.dumps(itemData, indent=4))
    except Exception as e:
        print(f"Error retrieving persistence data for {itemName}: {e}")

def testStoreItemData(persistenceAPI: Persistence, serviceID: str, itemName: str, time: str, state: str):
    """ Store persistence data for a specific item """
    print("\n~~~~ Test #7: storeItemData(itemName) ~~~~\n")

    try:
        response = persistenceAPI.storeItemData(serviceID, itemName, time, state)
        print("Data successfully stored:", response)
    except Exception as e:
        print(f"Error storing data for {itemName}: {e}")

def testDeleteItemData(persistenceAPI: Persistence, serviceID: str, itemName: str, startTime: str, endTime: str):
    """ Delete persistence data for a specific item """
    print("\n~~~~ Test #8: deleteItemData(itemName) ~~~~\n")

    try:
        response = persistenceAPI.deleteItemData(serviceID, itemName, startTime, endTime)
        print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error deleting persistence data for {itemName}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    persistenceAPI = Persistence(client)

    # Test variables
    service_id = "mapdb"
    item_name = "TemperatureSensor1"
    test_config = {"retention": "30d"}
    start_time = "2025-01-01T00:00:00.000Z"
    end_time = "2025-01-31T23:59:59.999Z"
    test_time = "2025-01-27T15:30:00.000Z"
    test_state = "22.5"

    # Run tests
    testGetAllPersistenceServices(persistenceAPI)                                           # Test #1
    testGetServiceConfiguration(persistenceAPI, service_id)                                 # Test #2
    testSetServiceConfiguration(persistenceAPI, service_id, test_config)                    # Test #3
    testDeleteServiceConfiguration(persistenceAPI, service_id)                              # Test #4
    testGetItemsForService(persistenceAPI, service_id)                                      # Test #5
    testGetItemPersistenceData(persistenceAPI, service_id, item_name, start_time, end_time) # Test #6
    testStoreItemData(persistenceAPI, service_id, item_name, test_time, test_state)         # Test #7
    testDeleteItemData(persistenceAPI, service_id, item_name, start_time, end_time)         # Test #8