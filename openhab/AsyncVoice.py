from .AsyncClient import AsyncOpenHABClient
import aiohttp
from typing import List, Optional


class AsyncVoice:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Async version of the Voice class.
        """
        self.client = client

    async def getDefaultVoice(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/voice/defaultvoice", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "No default voice was found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No default voice was found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getVoices(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/voice/voices", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    async def getInterpreters(self, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get("/voice/interpreters", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}

    async def getInterpreter(self, interpreterID: str, language: str = None):
        headers = {"Accept": "application/json"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.get(f"/voice/interpreters/{interpreterID}", headers=headers)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Interpreter not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Interpreter not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def interpretText(self, text: str, language: str = None):
        headers = {"Accept": "text/plain", "Content-Type": "text/plain"}
        if language:
            headers["Accept-Language"] = language

        try:
            response = await self.client.post("/voice/interpreters", headers=headers, data=text)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Interpretation exception occurs."}
            elif status_code == 404:
                return {"error": "No human language interpreter was found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Interpretation exception occurs."}
        elif status_code == 404:
            return {"error": "No human language interpreter was found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def interpretTextBatch(self, text: str, IDs: List[str], language: str = None):
        headers = {"Accept": "text/plain", "Content-Type": "text/plain"}
        if language:
            headers["Accept-Language"] = language

        params = {"ids": ",".join(IDs)}

        try:
            response = await self.client.post("/voice/interpreters", headers=headers, params=params, data=text)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Interpretation exception occurs."}
            elif status_code == 404:
                return {"error": "No human language interpreter was found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Interpretation exception occurs."}
        elif status_code == 404:
            return {"error": "No human language interpreter was found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def startDialog(
        self,
        sourceID: str,
        ksID: Optional[str] = None,
        sttID: Optional[str] = None,
        ttsID: Optional[str] = None,
        voiceID: Optional[str] = None,
        hliIDs: Optional[str] = None,
        sinkID: Optional[str] = None,
        keyword: Optional[str] = None,
        listeningItem: Optional[str] = None,
        language: Optional[str] = None,
    ):
        headers = {"Accept-Language": language} if language else {}
        params = {
            "sourceId": sourceID,
            "ksId": ksID,
            "sttId": sttID,
            "ttsId": ttsID,
            "voiceId": voiceID,
            "hliIds": hliIDs,
            "sinkId": sinkID,
            "keyword": keyword,
            "listeningItem": listeningItem,
        }

        try:
            response = await self.client.post("/voice/dialog/start", headers=headers, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Services missing, language not supported, or dialog already started."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Services missing, language not supported, or dialog already started."}

        return {"error": f"Unexpected response: {status_code}"}

    async def stopDialog(self, sourceID: str):
        params = {"sourceId": sourceID}

        try:
            response = await self.client.post("/voice/dialog/stop", params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 405:
                return {"error": "No dialog processing started for this audio source."}
            elif status_code == 404:
                return {"error": "No audio source found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "No audio source found."}
        elif status_code == 400:
            return {"error": "No dialog processing started for this audio source."}

        return {"error": f"Unexpected response: {status_code}"

        }

    async def listenAndAnswer(
        self,
        sourceID: str,
        sttID: str,
        ttsID: str,
        voiceID: str,
        hliIDs: List[str],
        sinkID: str,
        listeningItem: str,
        language: Optional[str] = None,
    ):
        headers = {"Accept-Language": language} if language else {}
        params = {
            "sourceId": sourceID,
            "sttId": sttID,
            "ttsId": ttsID,
            "voiceId": voiceID,
            "hliIds": ",".join(hliIDs) if hliIDs else None,
            "sinkId": sinkID,
            "listeningItem": listeningItem,
        }

        try:
            response = await self.client.post("/voice/listenandanswer", headers=headers, params=params)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Services missing, language not supported, or dialog already started."}
            elif status_code == 404:
                return {"error": "One of the given IDs is wrong."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Services missing, language not supported, or dialog already started."}
        elif status_code == 404:
            return {"error": "One of the given IDs is wrong."}

        return {"error": f"Unexpected response: {status_code}"}

    async def sayText(
        self,
        text: str,
        voiceID: str,
        sinkID: str,
        volume: str = "100",
    ):
        headers = {"Content-Type": "text/plain"}
        params = {"voiceId": voiceID, "sinkId": sinkID, "volume": volume}

        try:
            response = await self.client.post("/voice/say", headers=headers, params=params, data=text)

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}

        return {"error": f"Unexpected response: {status_code}"}
