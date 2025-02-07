from .Client import OpenHABClient
import json

class Tags:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Tags class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getTags(self, language=None):
        """
        Get all available semantic tags.

        :param language: Optional header for language setting.

        :return: A list of semantic tags (JSON).
        """
        return self.client.get("/tags", header={"Accept-Language": language} if language else {})

    def createTag(self, tagData, language=None):
        """
        Creates a new semantic tag and adds it to the registry.

        :param tagData: The data object for the tag to be created.
        :param language: Optional header for language setting.

        :return: The response to the tag creation request (JSON).
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.post("/tags", data=json.dumps(tagData), header=header)

    def getTag(self, tagID: str, language=None):
        """
        Gets a semantic tag and its sub-tags.

        :param tagID: The ID of the tag to retrieve.
        :param language: Optional header for language setting.

        :return: The tag object and its sub-tags (JSON).
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/tags/{tagID}", header=header)

    def updateTag(self, tagID: str, tagData, language=None):
        """
        Updates a semantic tag.

        :param tagID: The ID of the tag to be updated.
        :param tagData: The new tag data.
        :param language: Optional header for language setting.

        :return: The response to the tag update request (JSON).
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f"/tags/{tagID}", data=json.dumps(tagData), header=header)

    def deleteTag(self, tagID: str, language=None):
        """
        Removes a semantic tag and its sub-tags from the registry.

        :param tagID: The ID of the tag to be removed.
        :param language: Optional header for language setting.

        :return: The response to the tag deletion request (JSON).
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.delete(f"/tags/{tagID}", header=header)
