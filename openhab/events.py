from .client import OpenHABClient


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
        endpoint = "/events"
        params = {"topics": topics} if topics else {}
        try:
            return self.client.get(endpoint, params=params)
        except Exception as e:
            raise ValueError(f"Ungültige oder leere Topics: {e}")

    def initiate_state_tracker(self) -> str:
        """
        Startet eine neue Verbindung zum Verfolgen von Item-Statusänderungen.

        :return: Die Verbindungs-ID als String.
        """
        endpoint = "/events/states"
        return self.client.get(endpoint)

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

        endpoint = f"/events/states/{connection_id}"
        payload = items
        try:
            return self.client.post(endpoint, json=payload)
        except Exception as e:
            raise ValueError(f"Fehler beim Aktualisieren der Verbindung: {e}")


class ItemEvents:
    pass

"""
Event 	Description 	Topic
ItemAddedEvent 	An item has been added to the item registry. 	openhab/items/{itemName}/added
ItemRemovedEvent 	An item has been removed from the item registry. 	openhab/items/{itemName}/removed
ItemUpdatedEvent 	An item has been updated in the item registry. 	openhab/items/{itemName}/updated
ItemCommandEvent 	A command is sent to an item via a channel. 	openhab/items/{itemName}/command
ItemStateEvent 	The state of an item is updated. 	openhab/items/{itemName}/state
ItemStatePredictedEvent 	The state of an item predicted to be updated. 	openhab/items/{itemName}/statepredicted
ItemStateChangedEvent 	The state of an item has changed. 	openhab/items/{itemName}/statechanged
GroupItemStateChangedEvent 	The state of a group item has changed through a member. 	openhab/items/{itemName}/{memberName}/statechanged
"""

class ThingEvents:
    pass

"""
Event 	Description 	Topic
ThingAddedEvent 	A thing has been added to the thing registry. 	openhab/things/{thingUID}/added
ThingRemovedEvent 	A thing has been removed from the thing registry. 	openhab/things/{thingUID}/removed
ThingUpdatedEvent 	A thing has been updated in the thing registry. 	openhab/things/{thingUID}/updated
ThingStatusInfoEvent 	The status of a thing is updated. 	openhab/things/{thingUID}/status
ThingStatusInfoChangedEvent 	The status of a thing changed. 	openhab/things/{thingUID}/statuschanged
"""

class InboxEvents:
    pass

"""
Event 	Description 	Topic
InboxAddedEvent 	A discovery result has been added to the inbox. 	openhab/inbox/{thingUID}/added
InboxRemovedEvent 	A discovery result has been removed from the inbox. 	openhab/inbox/{thingUID}/removed
InboxUpdateEvent 	A discovery result has been updated in the inbox. 	openhab/inbox/{thingUID}/updated
"""

class LinkEvents:
    pass

"""
Event 	Description 	Topic
ItemChannelLinkAddedEvent 	An item channel link has been added to the registry. 	openhab/links/{itemName}-{channelUID}/added
ItemChannelLinkRemovedEvent 	An item channel link has been removed from the registry. 	openhab/links/{itemName}-{channelUID}/removed
"""

class ChannelEvents:
    pass

"""
Event 	Description 	Topic
ChannelDescriptionChangedEvent 	A dynamic CommandDescription or StateDescription has changed. 	openhab/channels/{channelUID}/descriptionchanged
ChannelTriggeredEvent 	A channel has been triggered. 	openhab/channels/{channelUID}/triggered
"""