from .client import OpenHABClient
import json

class Rules:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Rules class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getRules(self, prefix=None, tags=None, summary=False, staticDataOnly=False):
        """
        Get available rules, optionally filtered by tags and/or prefix.

        :param prefix: Optional prefix to filter the results.
        :param tags: Optional tag array to filter the results.
        :param summary: If true, only summary fields will be returned.
        :param staticDataOnly: If true, only static data will be returned.

        :return: A list of rules (JSON objects).
        """
        return self.client.get("/rules", params={"prefix": prefix, "tags": tags, "summary": summary, "staticDataOnly": staticDataOnly})

    def createRule(self, ruleData: dict):
        """
        Creates a rule.

        :param ruleData: The rule data to be created (as a dictionary).

        :return: The created rule (JSON).
        """
        return self.client.post("/rules", data=json.dumps(ruleData), header={"Content-Type": "application/json"})

    def getRule(self, ruleUID: str):
        """
        Gets the rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to retrieve.

        :return: The rule object (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}")

    def updateRule(self, ruleUID: str, ruleData: dict):
        """
        Updates an existing rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to update.
        :param ruleData: The new rule data (as a dictionary).

        :return: The updated rule (JSON).
        """
        return self.client.put(f"/rules/{ruleUID}", data=json.dumps(ruleData), header={"Content-Type": "application/json"})

    def deleteRule(self, ruleUID: str):
        """
        Removes an existing rule corresponding to the given UID.

        :param ruleUID: The UID of the rule to delete.

        :return: The API response (status code).
        """
        return self.client.delete(f"/rules/{ruleUID}", header={"Accept": "application/json"})

    def getModule(self, ruleUID: str, moduleCategory: str, moduleId: str):
        """
        Gets the rule's module corresponding to the given category and ID.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleId: The ID of the module.

        :return: The module (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/{moduleCategory}/{moduleId}", header={"Accept": "application/json"})

    def getModuleConfig(self, ruleUID: str, moduleCategory: str, moduleId: str):
        """
        Gets the module's configuration.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleId: The ID of the module.

        :return: The module configuration (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/{moduleCategory}/{moduleId}/config")

    def getModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleId: str, param: str):
        """
        Gets the module's configuration parameter.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleId: The ID of the module.
        :param param: The name of the configuration parameter.

        :return: The configuration parameter value (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/{moduleCategory}/{moduleId}/config/{param}", header={'Accept': 'text/plain'})

    def setModuleConfigParam(self, ruleUID: str, moduleCategory: str, moduleId: str, param: str, value: str):
        """
        Sets the module's configuration parameter value.

        :param ruleUID: The UID of the rule.
        :param moduleCategory: The category of the module.
        :param moduleId: The ID of the module.
        :param param: The name of the configuration parameter.
        :param value: The value to set for the configuration parameter.

        :return: The API response (status code).
        """
        return self.client.put(f"/rules/{ruleUID}/{moduleCategory}/{moduleId}/config/{param}", data=json.dumps(value), header={'Content-Type': 'text/plain'})

    def getActions(self, ruleUID: str):
        """
        Gets the rule actions.
        
        :param ruleUID: The UID of the rule.

        :return: A list of actions (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/actions")

    def getConditions(self, ruleUID: str):
        """
        Gets the rule conditions.

        :param ruleUID: The UID of the rule.

        :return: A list of conditions (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/conditions")

    def getConfiguration(self, ruleUID: str):
        """
        Gets the rule configuration values.
        
        :param ruleUID: The UID of the rule.

        :return: The configuration of the rule (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/config")

    def updateConfiguration(self, ruleUID: str, configData: dict):
        """
        Sets the rule configuration values.
        
        :param ruleUID: The UID of the rule.
        :param configData: The new configuration data (as a dictionary).

        :return: The updated configuration (JSON).
        """
        return self.client.put(f"/rules/{ruleUID}/config", data=json.dumps(configData), header={"Content-Type": "application/json"})

    def setRuleState(self, ruleUID: str, enable: bool):
        """
        Sets the rule configuration values. Activates or deactivates the rule.

        :param ruleUID: The UID of the rule.
        :param enable: If true, the rule will be activated. If false, the rule will be deactivated.

        :return: The API response (status code).
        """
        return self.client.post(f"/rules/{ruleUID}/enable", data="true" if enable else "false", header={"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"})

    def enableRule(self, ruleUID: str):
        return self.setRuleState(ruleUID, True)

    def disableRule(self, ruleUID: str):
        return self.setRuleState(ruleUID, False)

    def runNow(self, ruleUID: str, contextData: dict = None):
        """
        Executes the rule's actions immediately.

        :param ruleUID: The UID of the rule.
        :param contextData: Optional context data for executing the rule.

        :return: The API response (status code).
        """
        return self.client.post(f"/rules/{ruleUID}/runnow", data=json.dumps(contextData) or {})

    def getTriggers(self, ruleUID: str):
        """
        Gets the rule triggers.

        :param ruleUID: The UID of the rule.

        :return: A list of triggers (JSON).
        """
        return self.client.get(f"/rules/{ruleUID}/triggers")

    def simulateSchedule(self, fromTime: str, untilTime: str):
        """
        Simulates the executions of rules filtered by tag 'Schedule' within the given times.

        :param fromTime: Simulates the executions of rules filtered by tag 'Schedule' within the given times.
        :param untilTime: Simulates the executions of rules filtered by tag 'Schedule' within the given times.

        :return: The simulation results (JSON).
        """
        return self.client.get("/rules/schedule/simulations", params={"from": fromTime, "until": untilTime}, header={'Accept': 'application/json'})
