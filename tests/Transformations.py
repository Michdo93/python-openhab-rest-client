import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Transformations

def testGetTransformations(transformationsAPI: Transformations):
    """Retrieve all transformations"""
    print("\n~~~~ Test #1: getTransformations() ~~~~\n")

    try:
        transformations = transformationsAPI.getTransformations()
        print(json.dumps(transformations, indent=4))
    except Exception as e:
        print(f"Error retrieving transformations: {e}")

def testGetTransformation(transformationsAPI: Transformations, transformationUID: str):
    """Retrieve a specific transformation by transformationUID"""
    print("\n~~~~ Test #2: getTransformation(transformationUID) ~~~~\n")

    try:
        transformation = transformationsAPI.getTransformation(transformationUID)
        print(json.dumps(transformation, indent=4))
    except Exception as e:
        print(f"Error retrieving transformation {transformationUID}: {e}")

def testUpdateTransformation(transformationsAPI: Transformations, transformationUID: str, updatedData: dict):
    """Update a specific transformation by transformationUID"""
    print("\n~~~~ Test #3: updateTransformation(transformationUID, updatedData) ~~~~\n")

    try:
        response = transformationsAPI.updateTransformation(transformationUID, updatedData)
        print(f"Updated transformation {transformationUID}:\n{json.dumps(response, indent=4)}")
    except Exception as e:
        print(f"Error updating transformation {transformationUID}: {e}")

def testDeleteTransformation(transformationsAPI: Transformations, transformationUID: str):
    """Delete a specific transformation by transformationUID"""
    print("\n~~~~ Test #4: deleteTransformation(transformationUID) ~~~~\n")

    try:
        transformationsAPI.deleteTransformation(transformationUID)
        print(f"Transformation {transformationUID} deleted successfully.")
    except Exception as e:
        print(f"Error deleting transformation {transformationUID}: {e}")

def testGetTransformationServices(transformationsAPI: Transformations):
    """Retrieve all available transformation services"""
    print("\n~~~~ Test #5: getTransformationServices() ~~~~\n")

    try:
        services = transformationsAPI.getTransformationServices()
        print(json.dumps(services, indent=4))
    except Exception as e:
        print(f"Error retrieving transformation services: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    transformationsAPI = Transformations(client)

    # Example transformation transformationUID and updated data
    transformationUID = "en.map"
    updatedData = {
        "uid": "my_custom_map",
        "label": "My Custom Map",
        "type": "map",
        "configuration": {"function": "CLOSED=closed\nOPEN=open\nNULL=unknown\n"},
        "editable": True
    }

    # Execute test functions
    testGetTransformations(transformationsAPI)                                      # Test #1
    testGetTransformation(transformationsAPI, transformationUID)                    # Test #2
    testUpdateTransformation(transformationsAPI, transformationUID, updatedData)    # Test #3
    testDeleteTransformation(transformationsAPI, transformationUID)                 # Test #4
    testGetTransformationServices(transformationsAPI)                               # Test #5
