import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Audio

# Test the endpoint to get the default sink
def testGetDefaultSink(audioAPI: Audio, language: str = None):
    print("\n~~~~ Test #1 getDefaultSink() ~~~~\n")

    try:
        response = audioAPI.getDefaultSink(language)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to get the default source
def testGetDefaultSource(audioAPI: Audio, language: str = None):
    print("\n~~~~ Test #2 getDefaultSource() ~~~~\n")

    try:
        response = audioAPI.getDefaultSource(language)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to get all sinks
def testGetSinks(audioAPI: Audio, language: str = None):
    print("\n~~~~ Test #3 getSinks() ~~~~\n")

    try:
        response = audioAPI.getSinks(language)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

# Test the endpoint to get all sources
def testGetSources(audioAPI: Audio, language: str = None):
    print("\n~~~~ Test #4 getSources() ~~~~\n")

    try:
        response = audioAPI.getSources(language)
        print(response)
    except Exception as e:
        print(f"Error executing action: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    audioAPI = Audio(client)

    # Run all tests
    testGetDefaultSink(audioAPI)    # Test #1
    testGetDefaultSource(audioAPI)  # Test #2
    testGetSinks(audioAPI)          # Test #3
    testGetSources(audioAPI)        # Test #4
