from .client import OpenHABClient
import json

class Things:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Things class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllThings(self, summary: bool = False, staticDataOnly: bool = False, language: str = None):
        """
        Get all available things.

        :param summary: If True, returns only the summary fields.
        :param staticDataOnly: If True, returns a cacheable list.
        :param language: The preferred language for the response.

        :return: JSON response with the things.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get('/things', params={'summary': summary, 'staticDataOnly': staticDataOnly}, header=header)

    def createThing(self, thingData: dict, language: str = None):
        """
        Creates a new thing and adds it to the registry.

        :param thingData: The JSON object containing the thing data.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.post('/things', data=json.dumps(thingData), header=header)

    def getThingByUID(self, thingUID: str, language: str = None):
        """
        Gets a thing by UID.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing data.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f'/things/{thingUID}', header=header)

    def updateThing(self, thingUID: str, thingData: dict, language: str = None):
        """
        Updates a thing.

        :param thingUID: The UID of the thing.
        :param thingData: The JSON object containing the updated thing data.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f'/things/{thingUID}', data=json.dumps(thingData), header=header)

    def deleteThing(self, thingUID: str, force: bool = False, language: str = None):
        """
        Removes a thing from the registry. Set 'force' to __true__ if you want the thing to be removed immediately.

        :param thingUID: The UID of the thing.
        :param force: If True, the thing will be immediately removed.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        return self.client.delete(f'/things/{thingUID}', params={'force': force}, header={'Accept-Language': language} if language else {})

    def updateThingConfiguration(self, thingUID: str, configurationData: dict, language: str = None):
        """
        Updates a thing's configuration.

        :param thingUID: The UID of the thing.
        :param configurationData: The configuration data of the thing.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f'/things/{thingUID}/config', data=json.dumps(configurationData), header=header)

    def getThingConfigStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's configuration status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing's configuration status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f'/things/{thingUID}/config/status', header=header)
    
    def setThingStatus(self, thingUID: str, enabled: bool, language: str = None):
        """
        Sets the thing's enabled status.

        :param thingUID: The UID of the thing.
        :param enabled: If True, the thing will be enabled.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "text/plain"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f'/things/{thingUID}/enable', data="true" if enabled else "false", header=header)

    def enableThing(self, thingUID: str):
        return self.setThingStatus(thingUID, True)
    
    def disableThing(self, thingUID: str):
        return self.setThingStatus(thingUID, False)

    def updateThingFirmware(self, thingUID: str, firmwareVersion: str, language: str = None):
        """
        Updates the firmware of a thing.

        :param thingUID: The UID of the thing.
        :param firmwareVersion: The firmware version.
        :param language: The preferred language for the response.

        :return: The API response.
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f'/things/{thingUID}/firmware/{firmwareVersion}', header=header)

    def getThingFirmwareStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's firmware status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the firmware status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f'/things/{thingUID}/firmware/status', header=header)

    def getThingFirmwares(self, thingUID: str, language: str = None):
        """
        Gets all available firmwares for the provided thing UID.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: A list of available firmwares.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f'/things/{thingUID}/firmwares', header=header)

    def getThingStatus(self, thingUID: str, language: str = None):
        """
        Gets the thing's status.

        :param thingUID: The UID of the thing.
        :param language: The preferred language for the response.

        :return: JSON response with the thing's status.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f'/things/{thingUID}/status', header=header)
