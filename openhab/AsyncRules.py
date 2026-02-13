from .AsyncClient import AsyncOpenHABClient
import json
import aiohttp
from typing import Optional, List, Dict


class AsyncRules:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncRules class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getRules(self, prefix=None, tags=None, summary=False, staticDataOnly=False):
        """
        Get available rules, optionally filtered by tags and/or prefix.
        """
        params = {
            "prefix": prefix,
            "tags": tags,
            "summary": summary,
            "staticDataOnly": staticDataOnly
        }

        try:
            response = await self.client.get("/rules", params=params, headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def createRule(self, ruleData: dict):
        """
        Creates a new rule.
        """
        try:
            response = await self.client.post("/rules", data=json.dumps(ruleData),
                                              headers={"Content-Type": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Creation refused: Missing required parameter."}
            elif err.status == 409:
                return {"error": "Creation refused: Rule with the same UID already exists."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getRule(self, ruleUID: str):
        """
        Gets a rule by UID.
        """
        try:
            response = await self.client.get(f"/rules/{ruleUID}", headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Rule not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateRule(self, ruleUID: str, ruleData: dict):
        """
        Updates an existing rule.
        """
        try:
            response = await self.client.put(f"/rules/{ruleUID}", data=json.dumps(ruleData),
                                             headers={"Content-Type": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Rule corresponding to the given UID not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def deleteRule(self, ruleUID: str):
        """
        Deletes a rule by UID.
        """
        try:
            response = await self.client.delete(f"/rules/{ruleUID}")
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Rule corresponding to the given UID not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def runNow(self, ruleUID: str, contextData: dict = None):
        """
        Executes the rule's actions immediately.
        """
        try:
            data = json.dumps(contextData) if contextData else "{}"
            response = await self.client.post(f"/rules/{ruleUID}/runnow", data=data,
                                              headers={"Accept": "application/json"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Rule corresponding to the given UID not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def enable(self, ruleUID: str):
        return await self.setRuleState(ruleUID, True)

    async def disable(self, ruleUID: str):
        return await self.setRuleState(ruleUID, False)

    async def setRuleState(self, ruleUID: str, enable: bool):
        """
        Enables or disables a rule.
        """
        try:
            data = "true" if enable else "false"
            response = await self.client.post(f"/rules/{ruleUID}/enable", data=data,
                                              headers={"Content-Type": "text/plain"})
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Rule corresponding to the given UID not found."}
            else:
                return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def getModule(self, ruleUID: str, moduleCategory: str, moduleID: str):
        try:
            response = await self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}", headers={"Accept": "application/json"}
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule/module not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule/module not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getModuleConfig(self, ruleUID: str, moduleCategory: str, moduleID: str):
        try:
            response = await self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config", headers={"Accept": "application/json"}
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule/module not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule/module not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleID: str, param: str):
        try:
            response = await self.client.get(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config/{param}", headers={'Accept': 'text/plain'}
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule/module/config param not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule/module/config param not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def setModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleID: str, param: str, value: str):
        try:
            response = await self.client.put(
                f"/rules/{ruleUID}/{moduleCategory}/{moduleID}/config/{param}",
                data=json.dumps(value),
                headers={'Content-Type': 'text/plain'}
            )

            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response

        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule/module/config param not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}

        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule/module/config param not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getActions(self, ruleUID: str):
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get(f"/rules/{ruleUID}/actions", headers=headers)
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}
        return {"error": f"Unexpected response: {status_code}"}

    async def getConditions(self, ruleUID: str):
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get(f"/rules/{ruleUID}/conditions", headers=headers)
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}
        return {"error": f"Unexpected response: {status_code}"}

    async def getConfiguration(self, ruleUID: str):
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get(f"/rules/{ruleUID}/config", headers=headers)
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}
        return {"error": f"Unexpected response: {status_code}"}

    async def updateConfiguration(self, ruleUID: str, configData: dict):
        try:
            response = await self.client.put(
                f"/rules/{ruleUID}/config",
                data=json.dumps(configData),
                headers={"Content-Type": "application/json"}
            )
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}

        return {"error": f"Unexpected response: {status_code}"}

    async def getTriggers(self, ruleUID: str):
        headers = {"Accept": "application/json"}
        try:
            response = await self.client.get(f"/rules/{ruleUID}/triggers", headers=headers)
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 404:
                return {"error": "Rule not found."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if isinstance(response, dict) and "status" in response:
            status_code = response["status"]
        else:
            return response

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 404:
            return {"error": "Rule not found."}
        return {"error": f"Unexpected response: {status_code}"}

    async def simulateSchedule(self, fromTime: str, untilTime: str):
        try:
            response = await self.client.get(
                "/rules/schedule/simulations",
                params={"from": fromTime, "until": untilTime},
                headers={'Accept': 'application/json'}
            )
            if isinstance(response, dict) and "status" in response:
                status_code = response["status"]
            else:
                return response
        except aiohttp.ClientResponseError as err:
            status_code = err.status
            if status_code == 400:
                return {"error": "Max. simulation duration of 180 days exceeded."}
            return {"error": f"HTTP error {status_code}: {str(err)}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

        if status_code == 200:
            return {"message": "OK"}
        elif status_code == 400:
            return {"error": "Max. simulation duration of 180 days exceeded."}

        return {"error": f"Unexpected response: {status_code}"}