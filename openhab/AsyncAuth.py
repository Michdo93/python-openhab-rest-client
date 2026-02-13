from urllib.parse import urlencode
from .AsyncClient import AsyncOpenHABClient
import aiohttp


class AsyncAuth:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Async version of the Auth class.
        """
        self.client = client

    async def getAPITokens(self) -> dict:
        headers = {"Accept": "application/json"}

        try:
            response = await self.client.get("/auth/apitokens", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                return {"error": "User is not authenticated."}
            elif err.status == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    async def revokeAPIToken(self, tokenName: str) -> dict:
        try:
            response = await self.client.delete(f"/auth/apitokens/{tokenName}")

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                return {"error": "User is not authenticated."}
            elif err.status == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    async def logout(self, refreshToken: str, sessionID: str) -> dict:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "refresh_token": refreshToken,
            "id": sessionID
        }

        try:
            response = await self.client.post(
                "/auth/logout", headers=headers, data=data
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                return {"error": "User is not authenticated."}
            elif err.status == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getSessions(self) -> dict:
        headers = {"Accept": "application/json"}

        try:
            response = await self.client.get("/auth/sessions", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                return {"error": "User is not authenticated."}
            elif err.status == 404:
                return {"error": "User not found."}
            else:
                return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "User not found."}
        elif status_code == 401:
            return {"error": "User is not authenticated."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getToken(
        self,
        useCookie: bool = False,
        grantType: str = None,
        code: str = None,
        redirectURI: str = None,
        clientID: str = None,
        refreshToken: str = None,
        codeVerifier: str = None
    ) -> dict:

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        params = {
            "useCookie": str(useCookie).lower()
        }

        body = {
            "grant_type": grantType,
            "code": code,
            "redirect_uri": redirectURI,
            "client_id": clientID,
            "refresh_token": refreshToken,
            "code_verifier": codeVerifier
        }

        body = {k: v for k, v in body.items() if v is not None}

        encodedBody = urlencode(body)

        try:
            response = await self.client.post(
                "/auth/token",
                headers=headers,
                data=encodedBody,
                params=params
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Invalid request parameters."}
            else:
                return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return response
        elif status_code == 400:
            return {"error": "Invalid request parameters."}

        return {"error": f"Unexpected response: {status_code}"}
