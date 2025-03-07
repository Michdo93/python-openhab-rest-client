from .Client import OpenHABClient
import requests


class Discovery:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Discovery class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getDiscoveryBindings(self) -> list:
        """
        Gets all bindings that support discovery.

        :return: Eine Liste der Bindings als Strings.
        """
        try:
            response = self.client.get("/discovery", header={"Accept": "application/json"})

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    def getBindingInfo(self, bindingID: str, language: str = None) -> dict:
        """
        Gets information about the discovery services for a binding.

        :param bindingId: The ID of the binding to get discovery information for.
        :param language: Optional language parameter for the response (Accept-Language header).

        :return: Information about the discovery service for the specified binding.
        """
        header = {"Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        try:
            response = self.client.get(
                f"/discovery/bindings/{bindingID}/info", header=header)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                return {"error": "Discovery service not found."}
            elif status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return response

        return {"error": f"Unexpected response: {status_code}"}

    def startBindingScan(self, bindingID: str, input: str = None) -> int:
        """
        Starts asynchronous discovery process for a binding and returns the timeout in seconds of the discovery operation.

        :param bindingID: The ID of the binding for which the discovery is to be started.
        :param input: An input parameter to start the discovery.

        :return: Timeout duration of the discovery operation in seconds.
        """
        params = {
            "input": input
        }

        try:
            response = self.client.post(
                f"/discovery/bindings/{bindingID}/scan", header={"Accept": "text/plain"}, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            if status_code != 200:
                return {"error": f"HTTP error {status_code}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
