import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Voice

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
voice_api = Voice(client)

# Beispiele für die Voice-API
def voice_examples():
    # 1. Standardstimme abrufen
    default_voice = voice_api.get_default_voice()
    print("Default Voice:", default_voice)

    # 2. Liste aller Stimmen abrufen
    all_voices = voice_api.get_voices()
    print("All Voices:", all_voices)

    # 3. Eine spezifische Stimme abrufen
    if all_voices:
        voice_id = all_voices[0]['id']
        voice_details = voice_api.get_voice(voice_id)
        print(f"Details for Voice {voice_id}:", voice_details)

    # 4. Text mit einer Stimme ausgeben
    if all_voices:
        voice_id = all_voices[0]['id']
        response = voice_api.say_text("Hello from OpenHAB!", voice_id=voice_id, sink_id="default")
        print(f"Text spoken using Voice {voice_id}:", response)

    # 5. Interpreter abrufen
    interpreters = voice_api.get_interpreters(language="en")
    print("Interpreters:", interpreters)

    # 6. Text interpretieren
    interpreted_text = voice_api.interpret_text("Turn on the lights", language="en")
    print("Interpreted Text:", interpreted_text)

    # 7. Mehrere Interpreter zur Interpretation ansprechen
    if interpreters and 'id' in interpreters[0]:
        interpreter_ids = [interpreters[0]['id'], interpreters[1]['id']] if len(interpreters) > 1 else [interpreters[0]['id']]
        interpreted_text_batch = voice_api.interpret_text_batch("Turn off the heater", language="en", ids=interpreter_ids)
        print("Batch Interpreted Text:", interpreted_text_batch)

    # 8. Details eines einzelnen Interpreters abrufen
    if interpreters:
        interpreter_id = interpreters[0]['id']
        interpreter_details = voice_api.get_interpreter(interpreter_id, language="en")
        print(f"Interpreter details for {interpreter_id}:", interpreter_details)

    # 9. Dialog starten
    dialog_response = voice_api.start_dialog(
        source_id="audioSource1", 
        keyword="Hello", 
        stt_id="sttSystem", 
        tts_id="ttsSystem", 
        voice_id="voice1", 
        sink_id="audioOut"
    )
    print("Dialog started:", dialog_response)

    # 10. Dialog stoppen
    dialog_stop_response = voice_api.stop_dialog(source_id="audioSource1")
    print("Dialog stopped:", dialog_stop_response)

    # 11. Dialog ausführen (Listen and Answer)
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

# Funktion ausführen
if __name__ == "__main__":
    voice_examples()
