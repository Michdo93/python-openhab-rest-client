import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Persistence

class PersistenceTest:
    def __init__(self, client: OpenHABClient):
        self.persistenceAPI = Persistence(client)

    def testGetServices(self, language: str = None):
        """ Retrieve all available persistence services """
        print("\n~~~~ Test #1: getServices() ~~~~\n")

        try:
            services = self.persistenceAPI.getServices(language)
            print(json.dumps(services, indent=4))
        except Exception as e:
            print(f"Error retrieving persistence services: {e}")

    def testGetServiceConfiguration(self, serviceID: str):
        """ Retrieve the configuration of a specific persistence service """
        print("\n~~~~ Test #2: getServiceConfiguration(serviceID) ~~~~\n")

        try:
            config = self.persistenceAPI.getServiceConfiguration(serviceID)
            print(json.dumps(config, indent=4))
        except Exception as e:
            print(f"Error retrieving configuration for {serviceID}: {e}")

    def testSetServiceConfiguration(self, serviceID: str, config: dict):
        """ Update the configuration of a persistence service """
        print("\n~~~~ Test #3: setServiceConfiguration(serviceID, config) ~~~~\n")

        try:
            updatedConfig = self.persistenceAPI.setServiceConfiguration(serviceID, config)
            print(json.dumps(updatedConfig, indent=4))
        except Exception as e:
            print(f"Error updating configuration for {serviceID}: {e}")

    def testDeleteServiceConfiguration(self, serviceID: str):
        """ Delete the configuration of a persistence service """
        print("\n~~~~ Test #4: deleteServiceConfiguration(serviceID) ~~~~\n")

        try:
            response = self.persistenceAPI.deleteServiceConfiguration(serviceID)
            print(json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error deleting configuration for {serviceID}: {e}")

    def testGetItemsFromService(self, serviceID: str = None):
        """ Retrieve all items stored by a specific persistence service """
        print("\n~~~~ Test #5: getItemsFromService(serviceID) ~~~~\n")

        try:
            items = self.persistenceAPI.getItemsFromService(serviceID)
            print(json.dumps(items, indent=4))
        except Exception as e:
            print(f"Error retrieving items for service {serviceID}: {e}")

    def testGetItemPersistenceData(self, itemName: str, serviceID: str, startTime: str = None, endTime: str = None, page: int = 1, pageLength: int = 50, boundary: bool = False, itemState: bool = False):
        """ Retrieve persistence data for a specific item """
        print("\n~~~~ Test #6: getItemPersistenceData(itemName, serviceID) ~~~~\n")

        try:
            itemData = self.persistenceAPI.getItemPersistenceData(itemName, serviceID, startTime, endTime, page, pageLength, boundary, itemState)
            print(json.dumps(itemData, indent=4))
        except Exception as e:
            print(f"Error retrieving persistence data for {itemName}: {e}")

    def testStoreItemData(self, itemName: str, time: str, state: str, serviceID: str = None):
        """ Store persistence data for a specific item """
        print("\n~~~~ Test #7: storeItemData(itemName, time, state) ~~~~\n")

        try:
            response = self.persistenceAPI.storeItemData(itemName, time, state, serviceID)
            print("Data successfully stored:", response)
        except Exception as e:
            print(f"Error storing data for {itemName}: {e}")

    def testDeleteItemData(self, itemName: str, startTime: str, endTime: str, serviceID: str):
        """ Delete persistence data for a specific item """
        print("\n~~~~ Test #8: deleteItemData(itemName, startTime, endTime, serviceID) ~~~~\n")

        try:
            response = self.persistenceAPI.deleteItemData(itemName, startTime, endTime, serviceID)
            print(json.dumps(response, indent=4))
        except Exception as e:
            print(f"Error deleting persistence data for {itemName}: {e}")
