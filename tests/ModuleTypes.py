import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, ModuleTypes

def testGetAllModuleTypes(moduleTypesAPI: ModuleTypes, tags=None, typeFilter=None, language: str = None):
    """ Test retrieving all module types """
    print("\n~~~~ Test #1: getModuleTypes() ~~~~\n")
    try:
        moduleTypes = moduleTypesAPI.getModuleTypes(tags, typeFilter, language)
        print("All module types:", moduleTypes)
    except Exception as e:
        print(f"Error retrieving module types: {e}")

def testGetSingleModuleType(moduleTypesAPI: ModuleTypes, moduleTypeUID: str, language: str = None):
    """ Test retrieving a specific module type """
    print(f"\n~~~~ Test #2: getModuleType({moduleTypeUID}) ~~~~\n")
    try:
        moduleType = moduleTypesAPI.getModuleType(moduleTypeUID, language)
        print(f"Module type {moduleTypeUID}:", moduleType)
    except Exception as e:
        print(f"Error retrieving module type {moduleTypeUID}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    moduleTypesAPI = ModuleTypes(client)

    # Test variables
    moduleTypeUID = "timer.GenericCronTrigger"

    # Run tests
    testGetAllModuleTypes(moduleTypesAPI)
    testGetSingleModuleType(moduleTypesAPI, moduleTypeUID)
