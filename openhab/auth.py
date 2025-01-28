from urllib.parse import urlencode
from .client import OpenHABClient
import json

class Auth:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Auth-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_api_tokens(self, language: str = None) -> dict:
        """
        Listet alle API-Tokens des authentifizierten Benutzers auf.

        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = "/auth/apitokens"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)

    def revoke_api_token(self, token_name: str, language: str = None) -> dict:
        """
        Widerruft ein spezifisches API-Token des authentifizierten Benutzers.

        :param token_name: Name des API-Tokens, das widerrufen werden soll
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = f"/auth/apitokens/{token_name}"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.delete(endpoint, header=header)

    def logout(self, refresh_token: str, language: str = None) -> dict:
        """
        Meldet den Benutzer ab, indem die Session mit dem angegebenen Refresh-Token gelöscht wird.

        :param refresh_token: Der Refresh-Token, um die Session zu löschen
        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = "/auth/logout"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        if language:
            header["Accept-Language"] = language
        body = {"refresh_token": refresh_token}

        return self.client.post(endpoint, header=header, data=json.dumps(body))

    def get_sessions(self, language: str = None) -> dict:
        """
        Listet alle Sessions des authentifizierten Benutzers auf.

        :param language: (Optional) Spracheinstellung für die API-Anfrage
        :return: JSON-Antwort vom Server
        """
        endpoint = "/auth/sessions"
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)

    def get_token(self, grant_type: str, code: str = None, redirect_uri: str = None, client_id: str = None, refresh_token: str = None, code_verifier: str = None, language: str = None) -> dict:
        """
        Holt ein Access-Token und ein Refresh-Token, basierend auf den übergebenen Parametern.
        """
        endpoint = "/auth/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        body = {
            "grant_type": grant_type,
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "refresh_token": refresh_token,
            "code_verifier": code_verifier
        }
        # Entferne alle None-Werte
        body = {k: v for k, v in body.items() if v is not None}

        # Kodieren in application/x-www-form-urlencoded
        encoded_body = urlencode(body)

        return self.client.post(endpoint, header=header, data=encoded_body)

