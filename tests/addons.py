import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Addons

# Test the endpoint to retrieve all add-ons
def testGetAddons(addonsAPI: Addons, language: str = None):
    print("\n~~~~ Test #1 getAddons() ~~~~\n")

    try:
        response = addonsAPI.getAddons(language)
        print("Response from getAddons:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to retrieve a specific add-on
def testGetAddon(addonsAPI: Addons, addonID: str, language: str = None):
    print("\n~~~~ Test #2 getAddon(addonID) ~~~~\n")

    try:
        response = addonsAPI.getAddon(addonID, language)
        print(f"Response from getAddon for {addonID}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to install an add-on
def testInstallAddon(addonsAPI: Addons, addonID: str, language: str = None):
    print("\n~~~~ Test #3 installAddon(addonID) ~~~~\n")

    try:
        response = addonsAPI.installAddon(addonID, language)
        print(f"Response from installAddon for {addonID}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to uninstall an add-on
def testUninstallAddon(addonsAPI: Addons, addonID: str, language: str = None):
    print("\n~~~~ Test #4 uninstallAddon(addonID) ~~~~\n")

    try:
        response = addonsAPI.uninstallAddon(addonID, language)
        print(f"Response from uninstallAddon for {addonID}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to retrieve add-on types
def testGetAddonTypes(addonsAPI: Addons, language: str = None):
    print("\n~~~~ Test #5 getAddonTypes() ~~~~\n")

    try:
        response = addonsAPI.getAddonTypes(language)
        print("Response from getAddonTypes:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to retrieve recommended add-ons
def testGetAddonSuggestions(addonsAPI: Addons, language: str = None):
    print("\n~~~~ Test #6 getAddonSuggestions() ~~~~\n")

    try:
        response = addonsAPI.getAddonSuggestions(language)
        print("Response from getAddonSuggestions:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to retrieve add-on configuration
def testGetAddonConfig(addonsAPI: Addons, addonID: str):
    print("\n~~~~ Test #7 getAddonConfig(addonID) ~~~~\n")

    try:
        response = addonsAPI.getAddonConfig(addonID)
        print(f"Response from getAddonConfig for {addonID}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to update the add-on configuration
def testUpdateAddonConfig(addonsAPI: Addons, addonID: str, configData: dict):
    print("\n~~~~ Test #8 updateAddonConfig(addonID, configData) ~~~~\n")

    try:
        response = addonsAPI.updateAddonConfig(addonID, configData)
        print(f"Response from updateAddonConfig for {addonID}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to retrieve add-on services
def testGetAddonServices(addonsAPI: Addons, language: str = None):
    print("\n~~~~ Test #9 getAddonServices() ~~~~\n")

    try:
        response = addonsAPI.getAddonServices(language)
        print("Response from getAddonServices:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to install an add-on from a URL
def testInstallAddonFromUrl(addonsAPI: Addons, url: str):
    print("\n~~~~ Test #10 installAddonFromUrl(url) ~~~~\n")

    try:
        response = addonsAPI.installAddonFromUrl(url)
        print(f"Response from installAddonFromUrl for URL {url}:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error executing action: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    addonsAPI = Addons(client)

    addonID = "binding-astro"

    configData = {
        "latitude": 52.52,  # Berlin
        "longitude": 13.405, 
        "interval": 300  # Update every 5 minutes
    }
    
    # Replace this URL with a valid OpenHAB add-on URL
    url = "https://repo1.maven.org/maven2/org/smarthomej/addons/bundles/org.smarthomej.binding.amazonechocontrol/4.2.0/org.smarthomej.binding.amazonechocontrol-4.2.0.kar"
    
    # Run all tests
    testGetAddons(addonsAPI)                                # Test #1
    testGetAddon(addonsAPI, addonID)                        # Test #2
    testInstallAddon(addonsAPI, addonID)                    # Test #3
    testUninstallAddon(addonsAPI, addonID)                  # Test #4
    testGetAddonTypes(addonsAPI)                            # Test #5
    testGetAddonSuggestions(addonsAPI)                      # Test #6
    testGetAddonConfig(addonsAPI, addonID)                  # Test #7
    testUpdateAddonConfig(addonsAPI, addonID, configData)   # Test #8
    testGetAddonServices(addonsAPI)                         # Test #9
    testInstallAddonFromUrl(addonsAPI, url)                 # Test #10
