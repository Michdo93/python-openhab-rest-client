from .client import OpenHABClient
import json

class Logging:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Logging class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllLoggers(self) -> dict:
        """
        Get all loggers.

        :return: A list of loggers with names and levels.
        """        
        return self.client.get("/logging")

    def getSingleLogger(self, loggerName: str) -> dict:
        """
        Get a single logger.

        :param loggerName: The name of the logger.

        :return: The logger with the specified name and level.
        """        
        return self.client.get(f"/logging/{loggerName}")

    def modifyOrAddLogger(self, loggerName: str, level: str) -> dict:
        """
        Modify or add a logger.

        :param loggerName: The name of the logger.
        :param level: The level of the logger.

        :return: The API response after modification or addition.
        """
        data = {
            "loggerName": loggerName,
            "level": level
        }

        return self.client.put(f"/logging/{loggerName}", data=json.dumps(data), header={"Content-Type": "application/json"})

    def removeLogger(self, loggerName: str) -> dict:
        """
        Remove a single logger.

        :param loggerName: The name of the logger.

        :return: The API response after removing the logger.
        """        
        return self.client.delete(f"/logging/{loggerName}")
