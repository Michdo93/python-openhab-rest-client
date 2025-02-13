import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Logging

def testGetAllLoggers(loggingAPI: Logging):
    """ Test retrieving all loggers """
    print("\n~~~~ Test #1: getAllLoggers() ~~~~\n")
    try:
        loggers = loggingAPI.getAllLoggers()
        print("All loggers:", loggers)
    except Exception as e:
        print(f"Error retrieving loggers: {e}")

def testGetSingleLogger(loggingAPI: Logging, loggerName: str):
    """ Test retrieving a specific logger """
    print(f"\n~~~~ Test #2: getSingleLogger({loggerName}) ~~~~\n")
    try:
        logger = loggingAPI.getSingleLogger(loggerName)
        print(f"Logger {loggerName}:", logger)
    except Exception as e:
        print(f"Error retrieving logger {loggerName}: {e}")

def testModifyOrAddLogger(loggingAPI: Logging, loggerName: str, level: str):
    """ Test modifying or adding a logger """
    print(f"\n~~~~ Test #3: modifyOrAddLogger({loggerName}, {level}) ~~~~\n")
    try:
        response = loggingAPI.modifyOrAddLogger(loggerName, level)
        print(f"Logger {loggerName} modified:", response)
    except Exception as e:
        print(f"Error modifying logger {loggerName}: {e}")

def testRemoveLogger(loggingAPI: Logging, loggerName: str):
    """ Test removing a logger """
    print(f"\n~~~~ Test #4: removeLogger({loggerName}) ~~~~\n")
    try:
        response = loggingAPI.removeLogger(loggerName)
        print(f"Logger {loggerName} removed:", response)
    except Exception as e:
        print(f"Error removing logger {loggerName}: {e}")

if __name__ == "__main__":
    # Initialize OpenHAB client
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    loggingAPI = Logging(client)

    # Test variables
    loggerName = "org.openhab"
    loggerLevel = "DEBUG"

    # Run tests
    testGetAllLoggers(loggingAPI)                               # Test#1
    testGetSingleLogger(loggingAPI, loggerName)                 # Test#2
    testModifyOrAddLogger(loggingAPI, loggerName, loggerLevel)  # Test#3
    testRemoveLogger(loggingAPI, loggerName)                    # Test#4
