import sys
import os

# Füge den Projektwurzelpfad zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Voice

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
voice_api = Voice(client)

# Beispiele für die Voice-API mit Fehlerbehandlung
def voice_examples():
    try:
        # 1. Standardstimme abrufen
        print(1)
        default_voice = voice_api.get_default_voice()
        print("Default Voice:", default_voice)
    except Exception as e:
        print(f"Fehler beim Abrufen der Standardstimme: {e}")

    try:
        # 2. Liste aller Stimmen abrufen
        print(2)
        all_voices = voice_api.get_voices()
        print("All Voices:", all_voices)
    except Exception as e:
        print(f"Fehler beim Abrufen aller Stimmen: {e}")
        all_voices = []

    try:
        # 3. Text mit einer Stimme ausgeben
        print(3)
        if all_voices:
            voice_id = all_voices[0]['id']
            response = voice_api.say_text("Hello from OpenHAB!", voice_id=voice_id, sink_id="your_audio_sink_id")
            print(f"Text spoken using Voice {voice_id}:", response)
    except Exception as e:
        print(f"Fehler beim Sprechen des Textes: {e}")

    try:
        # 4. Liste aller Interpreter abrufen
        print(4)
        interpreters = voice_api.get_interpreters(language="en")
        print("Interpreters:", interpreters)
    except Exception as e:
        print(f"Fehler beim Abrufen der Interpreter: {e}")
        interpreters = []

    try:
        # 5. Text interpretieren (Standard-Interpreter)
        print(5)
        interpreted_text = voice_api.interpret_text("Turn on the lights", language="en", ids=[])
        print("Interpreted Text:", interpreted_text)
    except Exception as e:
        print(f"Fehler beim Interpretieren des Textes: {e}")

    try:
        # 6. Mehrere Interpreter zur Interpretation ansprechen
        print(6)
        if interpreters:
            interpreter_ids = [interpreter['id'] for interpreter in interpreters[:2]]  # Max. 2 Interpreter
            interpreted_text_batch = voice_api.interpret_text_batch("Turn off the heater", language="en", ids=interpreter_ids)
            print("Batch Interpreted Text:", interpreted_text_batch)
    except Exception as e:
        print(f"Fehler beim Batch-Interpretieren des Textes: {e}")

    try:
        # 7. Details eines einzelnen Interpreters abrufen
        print(7)
        if interpreters:
            interpreter_id = interpreters[0]['id']
            interpreter_details = voice_api.get_interpreter(interpreter_id, language="en")
            print(f"Interpreter details for {interpreter_id}:", interpreter_details)
    except Exception as e:
        print(f"Fehler beim Abrufen des Interpreters: {e}")

    try:
        print(8)
        # 8. Dialog starten
        dialog_response = voice_api.start_dialog(
            source_id="audioSource1", 
            keyword="Hello", 
            stt_id="sttSystem", 
            tts_id="ttsSystem", 
            voice_id="voice1", 
            sink_id="audioOut"
        )
        print("Dialog started:", dialog_response)
    except Exception as e:
        print(f"Fehler beim Starten des Dialogs: {e}")

    try:
        # 9. Dialog stoppen
        print(9)
        dialog_stop_response = voice_api.stop_dialog(source_id="audioSource1")
        print("Dialog stopped:", dialog_stop_response)
    except Exception as e:
        print(f"Fehler beim Stoppen des Dialogs: {e}")

    try:
        # 10. Listen and Answer ausführen
        print(10)
        listen_and_answer_response = voice_api.listen_and_answer(
            source_id="audioSource1", 
            stt_id="sttSystem", 
            tts_id="ttsSystem", 
            voice_id="voice1", 
            hli_ids=["interpreter1", "interpreter2"], 
            sink_id="audioOut", 
            listening_item="light_switch"
        )
        print("Listen and Answer response:", listen_and_answer_response)
    except Exception as e:
        print(f"Fehler bei Listen and Answer: {e}")

# Funktion ausführen
if __name__ == "__main__":
    voice_examples()
