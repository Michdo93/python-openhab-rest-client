from .Client import OpenHABClient

class Audio:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Audio class with an OpenHABClient object.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getDefaultSink(self, language: str = None):
        """
        Retrieves the default sink if defined, or the first available sink.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary containing information about the default sink.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/defaultsink", header=header)

    def getDefaultSource(self, language: str = None):
        """
        Retrieves the default source if defined, or the first available source.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A dictionary containing information about the default source.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/defaultsource", header=header)

    def getSinks(self, language: str = None):
        """
        Retrieves a list of all available sinks.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of available sinks.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/sinks", header=header)

    def getSources(self, language: str = None):
        """
        Retrieves a list of all available sources.

        :param language: (Optional) Language setting for the Accept-Language header.

        :return: A list of available sources.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/audio/sources", header=header)
