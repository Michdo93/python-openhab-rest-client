from .client import OpenHABClient
import json

class Events:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Events-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_events(self, topics: str = None) -> list:
        """
        Ruft alle verfügbaren Events ab, optional gefiltert nach Themen (Topics).

        :param topics: Eine durch Kommas getrennte Liste von Topics zum Filtern der Events.
        :return: Eine Liste von Events.
        :raises ValueError: Wenn das angegebene Topic leer oder ungültig ist.
        """
        return self.client._OpenHABClient__execute_sse(
            self.client.url + f"/rest/events" + (f"?topics={topics}" if topics else "")
        )

    def initiate_state_tracker(self) -> str:
        """
        Startet eine neue Verbindung zum Verfolgen von Item-Statusänderungen.

        :return: Die Verbindungs-ID als String.
        """
        url = self.client.url + "/rest/events/states"
        header = {"Accept": "*/*"}  # Wichtig!

        return self.client._OpenHABClient__execute_sse(url, header=header)

    def update_sse_connection_items(self, connection_id: str, items: list) -> str:
        """
        Aktualisiert die Liste von Items, für die eine SSE-Verbindung Statusaktualisierungen erhält.

        :param connection_id: Die ID der bestehenden Verbindung.
        :param items: Eine Liste von Item-Namen, für die Statusaktualisierungen abonniert werden sollen.
        :return: Eine Erfolgsnachricht, wenn die Aktualisierung abgeschlossen ist.
        :raises ValueError: Wenn die Verbindung oder die Liste der Items ungültig ist.
        """
        if not connection_id:
            raise ValueError("Die Verbindungs-ID darf nicht leer sein.")
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            raise ValueError("Die Items-Liste muss eine Liste von Strings sein.")

        endpoint = f"/rest/events/states/{connection_id}"  # Korrekte API-URL
        header = {"Content-Type": "application/json"}  # WICHTIG!
        
        payload = json.dumps(items)  # JSON korrekt formatieren
        
        try:
            return self.client.post(endpoint, data=payload, header=header)
        except Exception as e:
            raise ValueError(f"Fehler beim Aktualisieren der Verbindung: {e}")

class ItemEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Events-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def ItemEvent(self):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items")

    def ItemAddedEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/added")

    def ItemRemovedEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/removed")

    def ItemUpdatedEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/updated")

    def ItemCommandEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/command")

    def ItemStateEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/state")

    def ItemStatePredictedEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

    def ItemStateChangedEvent(self, itemName: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statechanged")

    def GroupItemStateChangedEvent(self, itemName: str, memberName: str):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")

class ThingEvents:
    def __init__(self, client: OpenHABClient):
        """Initialisiert die ThingEvents-Klasse mit einem OpenHABClient-Objekt."""
        self.client = client

    def ThingAddedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/added")

    def ThingRemovedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/removed")

    def ThingUpdatedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/updated")

    def ThingStatusInfoEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/status")

    def ThingStatusInfoChangedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/statuschanged")

class InboxEvents:
    def __init__(self, client: OpenHABClient):
        """Initialisiert die InboxEvents-Klasse mit einem OpenHABClient-Objekt."""
        self.client = client

    def InboxAddedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/added")

    def InboxRemovedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/removed")

    def InboxUpdatedEvent(self, thingUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/updated")

class LinkEvents:
    def __init__(self, client: OpenHABClient):
        """Initialisiert die LinkEvents-Klasse mit einem OpenHABClient-Objekt."""
        self.client = client

    def ItemChannelLinkAddedEvent(self, itemName: str = "*", channelUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/added")

    def ItemChannelLinkRemovedEvent(self, itemName: str = "*", channelUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/removed")

class ChannelEvents:
    def __init__(self, client: OpenHABClient):
        """Initialisiert die ChannelEvents-Klasse mit einem OpenHABClient-Objekt."""
        self.client = client

    def ChannelDescriptionChangedEvent(self, channelUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/descriptionchanged")

    def ChannelTriggeredEvent(self, channelUID: str = "*"):
        return self.client._OpenHABClient__execute_sse(self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/triggered")
