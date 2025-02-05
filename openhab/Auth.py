from urllib.parse import urlencode
from .client import OpenHABClient
import json

class Auth:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Auth class with an OpenHABClient instance.

        :param client: An instance of OpenHABClient used for REST API communication.
        """
        self.client = client

    def getApiTokens(self, language: str = None) -> dict:
        """
        Retrieve the API tokens associated with the authenticated user.

        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/auth/apitokens", header=header)

    def revokeApiToken(self, tokenName: str, language: str = None) -> dict:
        """
        Revoke a specific API token associated with the authenticated user.

        :param tokenName: Name of the API token to be revoked.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.delete(f"/auth/apitokens/{tokenName}", header=header)

    def logout(self, refreshToken: str, language: str = None) -> dict:
        """
        Terminate the session associated with a refresh token.

        :param refreshToken: The refresh token used to delete the session.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        if language:
            header["Accept-Language"] = language

        return self.client.post("/auth/logout", header=header, data=json.dumps({"refresh_token": refreshToken}))

    def getSessions(self, language: str = None) -> dict:
        """
        Retrieve the sessions associated with the authenticated user.

        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get("/auth/sessions", header=header)

    def getToken(self, grantType: str, code: str = None, redirectUri: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None, language: str = None) -> dict:
        """
        Obtain access and refresh tokens.

        :param grantType: The type of grant being requested.
        :param code: (Optional) Authorization code for authentication.
        :param redirectUri: (Optional) Redirect URI for OAuth authentication.
        :param clientID: (Optional) Client ID for authentication.
        :param refreshToken: (Optional) Refresh token for token renewal.
        :param codeVerifier: (Optional) Code verifier for PKCE authentication.
        :param language: (Optional) Language setting for the API request.

        :return: JSON response from the server.
        """
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        body = {
            "grant_type": grantType,
            "code": code,
            "redirect_uri": redirectUri,
            "client_id": clientID,
            "refresh_token": refreshToken,
            "code_verifier": codeVerifier
        }
        # Remove all None values
        body = {k: v for k, v in body.items() if v is not None}

        # Encode as application/x-www-form-urlencoded
        encodedBody = urlencode(body)

        return self.client.post("/auth/token", header=header, data=encodedBody)
