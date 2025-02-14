import sys
import os
import json

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhab import OpenHABClient, Voice

def testGetDefaultVoice(voiceAPI: Voice):
    print("\n~~~~ Test #1: getDefaultVoice() ~~~~\n")

    try:
        defaultVoice = voiceAPI.getDefaultVoice()
        print(f"Default Voice: {defaultVoice}")
    except Exception as e:
        print(f"Error retrieving default voice: {e}")

def testGetVoices(voiceAPI: Voice):
    print("\n~~~~ Test #2: getVoices() ~~~~\n")

    try:
        voices = voiceAPI.getVoices()
        print(json.dumps(voices, indent=4))
        return voices
    except Exception as e:
        print(f"Error retrieving voices: {e}")
        return []

def testSayText(voiceAPI: Voice, text: str, voiceID: str, sinkID: str, volume: str = '100'):
    print("\n~~~~ Test #3: sayText(text, voiceID, sinkID, volume) ~~~~\n")

    try:
        response = voiceAPI.sayText(text, voiceID, sinkID, volume)
        print(f"Text spoken using Voice {voiceID}: {response}")
    except Exception as e:
        print(f"Error speaking text: {e}")

def testGetInterpreters(voiceAPI: Voice, language: str = None):
    print("\n~~~~ Test #4: getInterpreters(language) ~~~~\n")

    try:
        interpreters = voiceAPI.getInterpreters(language)
        print(json.dumps(interpreters, indent=4))
        return interpreters
    except Exception as e:
        print(f"Error retrieving interpreters: {e}")
        return []

def testInterpretText(voiceAPI: Voice, text: str, language: str, IDs: list = None):
    print("\n~~~~ Test #5: interpretText(text, language, IDs) ~~~~\n")

    try:
        result = voiceAPI.interpretText(text, language, IDs)
        print(f"Interpreted Text: {result}")
    except Exception as e:
        print(f"Error interpreting text: {e}")

def testInterpretTextBatch(voiceAPI: Voice, text: str, language: str, IDs: list):
    print("\n~~~~ Test #6: interpretTextBatch(text, language, IDs) ~~~~\n")

    try:
        result = voiceAPI.interpretTextBatch(text, language, IDs)
        print(f"Batch Interpreted Text: {result}")
    except Exception as e:
        print(f"Error batch interpreting text: {e}")

def testGetInterpreter(voiceAPI: Voice, interpreterID: str, language: str = None):
    print("\n~~~~ Test #7: getInterpreter(interpreterID, language) ~~~~\n")

    try:
        interpreter = voiceAPI.getInterpreter(interpreterID, language)
        print(f"Interpreter Details: {json.dumps(interpreter, indent=4)}")
    except Exception as e:
        print(f"Error retrieving interpreter: {e}")

def testStartDialog(voiceAPI: Voice, sourceID: str, keyword: str, sttID: str, ttsID: str, voiceID: str, sinkID: str):
    print("\n~~~~ Test #8: startDialog(sourceID, keyword, sttID, ttsID, voiceID, sinkID) ~~~~\n")

    try:
        response = voiceAPI.startDialog(sourceID, keyword, sttID, ttsID, voiceID, sinkID)
        print(f"Dialog started: {json.dumps(response, indent=4)}")
    except Exception as e:
        print(f"Error starting dialog: {e}")

def testStopDialog(voiceAPI: Voice, sourceID: str):
    print("\n~~~~ Test #9: stopDialog(sourceID) ~~~~\n")

    try:
        response = voiceAPI.stopDialog(sourceID)
        print(f"Dialog stopped: {json.dumps(response, indent=4)}")
    except Exception as e:
        print(f"Error stopping dialog: {e}")

def testListenAndAnswer(voiceAPI: Voice, sourceID: str, sttID: str, ttsID: str, voiceID: str, hliIDs: list, sinkID: str, listeningItem: str):
    print("\n~~~~ Test #10: listenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem) ~~~~\n")

    try:
        response = voiceAPI.listenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem)
        print(f"Listen and Answer Response: {json.dumps(response, indent=4)}")
    except Exception as e:
        print(f"Error with Listen and Answer: {e}")

if __name__ == "__main__":
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    voiceAPI = Voice(client)
    
    text = "Hello from OpenHAB!"
    language = "en"
    sourceID = "audioSource1"
    keyword = "Hello"
    sttID = "sttSystem"
    ttsID = "ttsSystem"
    voiceID = "voice1"
    sinkID = "audioOut"
    hliIDs = ["interpreter1", "interpreter2"]
    listeningItem = "light_switch"
    interpreterID = "interpreter1"
    
    voices = testGetVoices(voiceAPI)                                                                        # Test #1
    testGetDefaultVoice(voiceAPI)                                                                           # Test #2
    if voices:
        testSayText(voiceAPI, text, voices[0]["id"], sinkID)                                                # Test #3
    interpreters = testGetInterpreters(voiceAPI, language)                                                  # Test #4
    testInterpretText(voiceAPI, text, language, [])                                                         # Test #5
    if interpreters:
        testInterpretTextBatch(voiceAPI, text, language, [interp["id"] for interp in interpreters[:2]])     # Test #6
    testGetInterpreter(voiceAPI, interpreterID, language)                                                   # Test #7
    testStartDialog(voiceAPI, sourceID, keyword, sttID, ttsID, voiceID, sinkID)                             # Test #8
    testStopDialog(voiceAPI, sourceID)                                                                      # Test #9
    testListenAndAnswer(voiceAPI, sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem)           # Test #10
