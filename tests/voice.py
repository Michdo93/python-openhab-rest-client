import sys
import os

# Füge den Projektwurzelpfad zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Voice

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
voiceApi = Voice(client)

# Beispiele für die Voice-API mit Fehlerbehandlung
def voiceExamples():
    try:
        # 1. Standardstimme abrufen
        print(1)
        defaultVoice = voiceApi.getDefaultVoice()
        print("Default Voice:", defaultVoice)
    except Exception as e:
        print(f"Fehler beim Abrufen der Standardstimme: {e}")

    try:
        # 2. Liste aller Stimmen abrufen
        print(2)
        allVoices = voiceApi.getVoices()
        print("All Voices:", allVoices)
    except Exception as e:
        print(f"Fehler beim Abrufen aller Stimmen: {e}")
        allVoices = []

    try:
        # 3. Text mit einer Stimme ausgeben
        print(3)
        if allVoices:
            voiceId = allVoices[0]['id']
            response = voiceApi.sayText("Hello from OpenHAB!", voiceID=voiceId, sinkId="your_audio_sink_id")
            print(f"Text spoken using Voice {voiceId}:", response)
    except Exception as e:
        print(f"Fehler beim Sprechen des Textes: {e}")

    try:
        # 4. Liste aller Interpreter abrufen
        print(4)
        interpreters = voiceApi.getInterpreters(language="en")
        print("Interpreters:", interpreters)
    except Exception as e:
        print(f"Fehler beim Abrufen der Interpreter: {e}")
        interpreters = []

    try:
        # 5. Text interpretieren (Standard-Interpreter)
        print(5)
        interpretedText = voiceApi.interpretText("Turn on the lights", language="en", IDs=[])
        print("Interpreted Text:", interpretedText)
    except Exception as e:
        print(f"Fehler beim Interpretieren des Textes: {e}")

    try:
        # 6. Mehrere Interpreter zur Interpretation ansprechen
        print(6)
        if interpreters:
            interpreterIds = [interpreter['id'] for interpreter in interpreters[:2]]  # Max. 2 Interpreter
            interpretedTextBatch = voiceApi.interpretTextBatch("Turn off the heater", language="en", IDs=interpreterIds)
            print("Batch Interpreted Text:", interpretedTextBatch)
    except Exception as e:
        print(f"Fehler beim Batch-Interpretieren des Textes: {e}")

    try:
        # 7. Details eines einzelnen Interpreters abrufen
        print(7)
        if interpreters:
            interpreterId = interpreters[0]['id']
            interpreterDetails = voiceApi.getInterpreter(interpreterId, language="en")
            print(f"Interpreter details for {interpreterId}:", interpreterDetails)
    except Exception as e:
        print(f"Fehler beim Abrufen des Interpreters: {e}")

    try:
        print(8)
        # 8. Dialog starten
        dialogResponse = voiceApi.startDialog(
            sourceID="audioSource1", 
            keyword="Hello", 
            sttID="sttSystem", 
            ttsID="ttsSystem", 
            voiceID="voice1", 
            sinkID="audioOut"
        )
        print("Dialog started:", dialogResponse)
    except Exception as e:
        print(f"Fehler beim Starten des Dialogs: {e}")

    try:
        # 9. Dialog stoppen
        print(9)
        dialogStopResponse = voiceApi.stopDialog(sourceID="audioSource1")
        print("Dialog stopped:", dialogStopResponse)
    except Exception as e:
        print(f"Fehler beim Stoppen des Dialogs: {e}")

    try:
        # 10. Listen and Answer ausführen
        print(10)
        listenAndAnswerResponse = voiceApi.listenAndAnswer(
            sourceID="audioSource1", 
            sttID="sttSystem", 
            ttsID="ttsSystem", 
            voiceID="voice1", 
            hliIDs=["interpreter1", "interpreter2"], 
            sinkID="audioOut", 
            listeningItem="light_switch"
        )
        print("Listen and Answer response:", listenAndAnswerResponse)
    except Exception as e:
        print(f"Fehler bei Listen and Answer: {e}")

# Funktion ausführen
if __name__ == "__main__":
    voiceExamples()
