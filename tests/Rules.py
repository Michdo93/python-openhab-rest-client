import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Rules

def testGetAllRules(rulesAPI: Rules):
    """ Retrieve all rules """
    print("\n~~~~ Test #1 getRules() ~~~~\n")

    try:
        rules = rulesAPI.getRules()
        print(json.dumps(rules, indent=4))
    except Exception as e:
        print(f"Error retrieving rules: {e}")

def testGetRuleDetails(rulesAPI: Rules, ruleID: str):
    """ Retrieve details of a specific rule """
    print("\n~~~~ Test #2 getRule(ruleID) ~~~~\n")

    try:
        rule = rulesAPI.getRule(ruleID)
        print(json.dumps(rule, indent=4))
    except Exception as e:
        print(f"Error retrieving rule {ruleID}: {e}")

def testCreateRule(rulesAPI: Rules, rule_data: dict):
    """ Create a new rule """
    print("\n~~~~ Test #3 createRule(rule_data) ~~~~\n")

    try:
        rulesAPI.createRule(rule_data)
        print("New Rule created successfully.")
    except Exception as e:
        print(f"Error creating rule: {e}")

def testUpdateRule(rulesAPI: Rules, ruleID: str, updateData: dict):
    """ Update an existing rule """
    print("\n~~~~ Test #4 updateRule(ruleID, updateData) ~~~~\n")

    try:
        rulesAPI.updateRule(ruleID, updateData)
        print("Rule updated successfully.")
    except Exception as e:
        print(f"Error updating rule {ruleID}: {e}")

def testSetRuleState(rulesAPI: Rules, ruleID: str, state: bool):
    """ Enable or disable a rule """
    action = "enabled" if state else "disabled"
    print("\n~~~~ Test #5 setRuleState(ruleID, state) ~~~~\n")

    try:
        rulesAPI.setRuleState(ruleID, state)
        print(f"Rule {ruleID} {action}.")
    except Exception as e:
        print(f"Error setting rule state for {ruleID}: {e}")

def testDeleteRule(rulesAPI: Rules, ruleID: str):
    """ Delete a rule """
    print("\n~~~~ Test #6 deleteRule(ruleID) ~~~~\n")

    try:
        rulesAPI.deleteRule(ruleID)
        print("Rule deleted successfully.")
    except Exception as e:
        print(f"Error deleting rule {ruleID}: {e}")

def testExecuteRuleNow(rulesAPI: Rules, ruleID: str):
    """ Execute a rule immediately """
    print("\n~~~~ Test #7 runNow(ruleID) ~~~~\n")

    try:
        rulesAPI.runNow(ruleID)
        print("Rule executed successfully.")
    except Exception as e:
        print(f"Error executing rule {ruleID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    rulesAPI = Rules(client)

    # Example rule data
    ruleID = "test_color-1"
    newRuleData = {
        "uid": "newRule",
        "name": "New Rule",
        "description": "This is a new rule",
        "triggers": [],
        "conditions": [],
        "actions": []
    }
    updateData = {"name": "Updated Rule"}

    # Execute functions
    testGetAllRules(rulesAPI)                       # Test #1
    testGetRuleDetails(rulesAPI, ruleID)            # Test #2
    testCreateRule(rulesAPI, newRuleData)           # Test #3
    testUpdateRule(rulesAPI, "newRule", updateData) # Test #4
    testSetRuleState(rulesAPI, "newRule", True)     # Test #5
    testSetRuleState(rulesAPI, "newRule", False)    # Test #5
    testExecuteRuleNow(rulesAPI, ruleID)            # Test #6
    testDeleteRule(rulesAPI, "newRule")             # Test #7
