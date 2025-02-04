from .client import OpenHABClient
import json

class Voice:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Voice-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_default_voice(self):
        """
        Ruft die Standard-Stimme ab.

        :return: Ein Dictionary mit den Details der Standard-Stimme.
        """
        return self.client.get('/voice/defaultvoice')

    def start_dialog(self, source_id: str, ks_id: str = None, stt_id: str = None, 
                     tts_id: str = None, voice_id: str = None, hli_ids: str = None, 
                     sink_id: str = None, keyword: str = None, listening_item: str = None):
        """
        Startet die Dialogverarbeitung für eine gegebene Audioquelle.

        :param source_id: Die ID der Audioquelle.
        :param ks_id: Die ID des Keyword Spotters (optional).
        :param stt_id: Die ID des Speech-to-Text-Systems (optional).
        :param tts_id: Die ID des Text-to-Speech-Systems (optional).
        :param voice_id: Die ID der Stimme (optional).
        :param hli_ids: Eine durch Kommas getrennte Liste von Interpreter-IDs (optional).
        :param sink_id: Die ID des Audio-Ausgangs (optional).
        :param keyword: Das Keyword, das für das Dialogstarten verwendet wird (optional).
        :param listening_item: Der Name des zu hörenden Items (optional).
        :return: Die Antwort des Servers.
        """
        params = {
            'sourceId': source_id,
            'ksId': ks_id,
            'sttId': stt_id,
            'ttsId': tts_id,
            'voiceId': voice_id,
            'hliIds': hli_ids,
            'sinkId': sink_id,
            'keyword': keyword,
            'listeningItem': listening_item
        }
        return self.client.post('/voice/dialog/start', params=params)

    def stop_dialog(self, source_id: str):
        """
        Stoppt die Dialogverarbeitung für eine gegebene Audioquelle.

        :param source_id: Die ID der Audioquelle.
        :return: Die Antwort des Servers.
        """
        params = {'sourceId': source_id}
        return self.client.post('/voice/dialog/stop', params=params)

    def get_interpreters(self, language: str = None):
        """
        Ruft die Liste aller Interpreter ab.

        :param language: Die Sprache für die Anfrage (optional).
        :return: Eine Liste der Interpreter, wenn erfolgreich.
        """
        header = {'Accept-Language': language} if language else {}
        return self.client.get('/voice/interpreters', header=header)

    def interpret_text(self, text: str, language: str, ids: list = None):
        """
        Sendet Text zur Interpretation an den Standard-Interpreter oder an spezifische Interpreter.

        :param text: Der zu interpretierende Text.
        :param language: Die Sprache des Textes.
        :param ids: Eine Liste von Interpreter-IDs (optional).
        :return: Die Antwort des Servers.
        """
        header = {'Accept-Language': language}
        params = {'ids': ','.join(ids)} if ids else {}
        data = {'text': text}
        data = json.dumps(data)

        return self.client.post('/voice/interpreters', header=header, params=params, data=data)

    def get_interpreter(self, interpreter_id: str, language: str = None):
        """
        Ruft die Details eines einzelnen Interpreters ab.

        :param interpreter_id: Die ID des Interpreters.
        :param language: Die Sprache für die Anfrage (optional).
        :return: Die Details des Interpreters.
        """
        header = {'Accept-Language': language} if language else {}
        return self.client.get(f'/voice/interpreters/{interpreter_id}', header=header)

    def interpret_text_batch(self, text: str, language: str, ids: list):
        """
        Sendet Text zur Interpretation an mehrere spezifische Interpreter.

        :param text: Der zu interpretierende Text.
        :param language: Die Sprache des Textes.
        :param ids: Eine Liste von Interpreter-IDs.
        :return: Die Antwort des Servers.
        """
        header = {'Accept-Language': language}
        params = {'ids': ','.join(ids)}
        data = {'text': text}
        data = json.dumps(data)

        return self.client.post('/voice/interpreters', header=header, params=params, data=data)

    def listen_and_answer(self, source_id: str, stt_id: str, tts_id: str, voice_id: str,
                        hli_ids: list = None, sink_id: str = None, listening_item: str = None):
        """
        Führt eine einfache Dialogsequenz ohne Keyword-Spotting aus.

        :param source_id: Die ID der Audioquelle.
        :param stt_id: Die ID des Speech-to-Text-Systems.
        :param tts_id: Die ID des Text-to-Speech-Systems.
        :param voice_id: Die ID der Stimme.
        :param hli_ids: Eine Liste von Interpreter-IDs (optional).
        :param sink_id: Die ID des Audio-Ausgangs (optional).
        :param listening_item: Der Name des zu hörenden Items (optional).
        :return: Die Antwort des Servers.
        """
        params = {
            'sourceId': source_id,
            'sttId': stt_id,
            'ttsId': tts_id,
            'voiceId': voice_id,
            'hliIds': ','.join(hli_ids) if hli_ids else None,
            'sinkId': sink_id,
            'listeningItem': listening_item
        }
        return self.client.post('/voice/listenandanswer', params=params)

    def say_text(self, text: str, voice_id: str, sink_id: str, volume: str = '100'):
        """
        Spricht einen Text mit einer gegebenen Stimme über den angegebenen Audio-Ausgang.

        :param text: Der zu sprechende Text.
        :param voice_id: Die ID der Stimme.
        :param sink_id: Die ID des Audio-Ausgangs.
        :param volume: Die Lautstärke (Standard: 100).
        :return: Die Antwort des Servers.
        """
        params = {
            'voiceid': voice_id,
            'sinkid': sink_id,
            'volume': volume
        }
        data = {'text': text}
        data = json.dumps(data)

        return self.client.post('/voice/say', params=params, data=data)

    def get_voices(self):
        """
        Ruft die Liste aller verfügbaren Stimmen ab.

        :return: Eine Liste der Stimmen, wenn erfolgreich.
        """
        return self.client.get('/voice/voices')
