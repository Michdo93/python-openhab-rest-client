from .Client import OpenHABClient
import json

class Voice:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Voice class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getDefaultVoice(self):
        """
        Gets the default voice.

        :return: A dictionary with the details of the default voice.
        """
        return self.client.get('/voice/defaultvoice', header={"Accept": "application/json"})

    def startDialog(self, sourceID: str, ksID: str = None, sttID: str = None, 
                    ttsID: str = None, voiceID: str = None, hliIDs: str = None, 
                    sinkID: str = None, keyword: str = None, listeningItem: str = None):
        """
        Start dialog processing for a given audio source.

        :param sourceID: The ID of the audio source.
        :param ksID: The ID of the keyword spotter (optional).
        :param sttID: The ID of the speech-to-text system (optional).
        :param ttsID: The ID of the text-to-speech system (optional).
        :param voiceID: The ID of the voice (optional).
        :param hliIDs: A comma-separated list of interpreter IDs (optional).
        :param sinkID: The ID of the audio output (optional).
        :param keyword: The keyword used to start the dialog (optional).
        :param listeningItem: The name of the item to listen to (optional).
        
        :return: The response from the server.
        """
        return self.client.post('/voice/dialog/start', params={'sourceId': sourceID, 'ksId': ksID, 'sttID': sttID, 'ttsId': ttsID, 'voiceId': voiceID, 'hliIds': hliIDs, 'sinkId': sinkID, 'keyword': keyword, 'listeningItem': listeningItem})

    def stopDialog(self, sourceID: str):
        """
        Stop dialog processing for a given audio source.

        :param sourceID: The ID of the audio source.
        :return: The response from the server.
        """
        return self.client.post('/voice/dialog/stop', params={'sourceId': sourceID})

    def getInterpreters(self, language: str = None):
        """
        Get the list of all interpreters.

        :param language: The language for the request (optional).

        :return: A list of interpreters if successful.
        """
        header = {"Accept": "application/json"}
        if language:
            header["Accept-Language"] = language

        return self.client.get('/voice/interpreters', header=header)

    def interpretText(self, text: str, language: str, IDs: list = None):
        """
        Sends a text to the default human language interpreter.

        :param text: The text to be interpreted.
        :param language: The language of the text.
        :param IDs: A list of interpreter IDs (optional).

        :return: The response from the server.
        """
        header = {"Content-Type": "text/plain"}
        if language:
            header["Accept-Language"] = language

        return self.client.post('/voice/interpreters', header=header, params={'ids': ','.join(IDs)} if IDs else {}, data={'text': text})

    def getInterpreter(self, interpreterID: str, language: str = None):
        """
        Gets a single interpreter.

        :param interpreterID: The ID of the interpreter.
        :param language: The language for the request (optional).

        :return: The details of the interpreter.
        """
        header = {"Content-Type": "application/json"}
        if language:
            header["Accept-Language"] = language
        
        return self.client.get(f'/voice/interpreters/{interpreterID}', header=header)

    def interpretTextBatch(self, text: str, language: str, IDs: list):
        """
        Sends a text to a given human language interpreter(s).

        :param text: The text to be interpreted.
        :param language: The language of the text.
        :param IDs: A list of interpreter IDs.

        :return: The response from the server.
        """
        header = {"Content-Type": "text/plain"}
        if language:
            header["Accept-Language"] = language

        return self.client.post('/voice/interpreters', header=header, params={'ids': ','.join(IDs)}, data=json.dumps({'text': text}))

    def listenAndAnswer(self, sourceID: str, sttID: str, ttsID: str, voiceID: str,
                        hliIDs: list = None, sinkID: str = None, listeningItem: str = None):
        """
        Executes a simple dialog sequence without keyword spotting for a given audio source.

        :param sourceID: The ID of the audio source.
        :param sttID: The ID of the speech-to-text system.
        :param ttsID: The ID of the text-to-speech system.
        :param voiceID: The ID of the voice.
        :param hliIDs: A list of interpreter IDs (optional).
        :param sinkID: The ID of the audio output (optional).
        :param listeningItem: The name of the item to listen to (optional).
        
        :return: The response from the server.
        """
        return self.client.post('/voice/listenandanswer', data={'sourceId': sourceID, 'sttId': sttID, 'ttsId': ttsID, 'voiceId': voiceID, 'hliIds': ','.join(hliIDs) if hliIDs else None, 'sinkId': sinkID, 'listeningItem': listeningItem})

    def sayText(self, text: str, voiceID: str, sinkID: str, volume: str = '100'):
        """
        Speaks a given text with a given voice through the given audio sink.

        :param text: The text to be spoken.
        :param voiceID: The ID of the voice.
        :param sinkID: The ID of the audio output.
        :param volume: The volume level (default: 100).
        
        :return: The response from the server.
        """
        return self.client.post('/voice/say', params={'voiceId': voiceID, 'sinkId': sinkID, 'volume': volume}, data={'text': text}, header={"Content-Type": "text/plain"})

    def getVoices(self):
        """
        Get the list of all voices.

        :return: A list of voices if successful.
        """
        return self.client.get('/voice/voices', header={"Accept": "application/json"})
