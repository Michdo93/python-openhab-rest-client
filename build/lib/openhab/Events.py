from .Client import OpenHABClient
import json

class Events:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Events class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getAllEvents(self, topics: str = None) -> list:
        """
        Get all available events, optionally filtered by topic.

        :param topics: A comma-separated list of topics to filter the events by.

        :return: A SSE stream of events.
        """
        return self.client._OpenHABClient__executeSSE(
            self.client.url + f"/rest/events" + (f"?topics={topics}" if topics else "")
        )

    def initiateStateTracker(self) -> str:
        """
        Initiates a new item state tracker connection.

        :return: The connection ID as a string.
        """

        return self.client._OpenHABClient__executeSSE(self.client.url + "/rest/events/states", header={"Accept": "*/*"} )

    def updateSseConnectionItems(self, connectionId: str, items: list) -> str:
        """
        Changes the list of items a SSE connection will receive state updates for.

        :param connectionId: The ID of the existing connection.
        :param items: A SSE stream of item names to subscribe to for state updates.

        :return: A success message when the update is completed.
        """
                
        return self.client.post(f"/rest/events/states/{connectionId}", data=json.dumps(items), header={"Content-Type": "application/json"})

class ItemEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ItemEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ItemEvent(self):
        """
        Get all item-related events.

        :return: A SSE stream of item events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items")

    def ItemAddedEvent(self, itemName: str = "*"):
        """
        Get events for added items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of added item events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/added")

    def ItemRemovedEvent(self, itemName: str = "*"):
        """
        Get events for removed items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of removed item events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/removed")

    def ItemUpdatedEvent(self, itemName: str = "*"):
        """
        Get events for updated items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of updated item events.
        """

        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/updated")

    def ItemCommandEvent(self, itemName: str = "*"):
        """
        Get events for item commands.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item command events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/command")

    def ItemStateEvent(self, itemName: str = "*"):
        """
        Get events for item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state events.
        """

        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/state")

    def ItemStatePredictedEvent(self, itemName: str = "*"):
        """
        Get events for predicted item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state predicted events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

    def ItemStateChangedEvent(self, itemName: str = "*"):
        """
        Get events for item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state changed events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/statechanged")

    def GroupItemStateChangedEvent(self, itemName: str, memberName: str):
        """
        Get events for state changes of group items.

        :param itemName: The name of the item.
        :param memberName: The name of the group member.

        :return: A SSE stream of group item state changed events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")

class ThingEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ThingEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ThingAddedEvent(self, thingUID: str = "*"):
        """
        Get events for added things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of added thing events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/added")

    def ThingRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed thing events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/removed")

    def ThingUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated thing events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/updated")

    def ThingStatusInfoEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/status")

    def ThingStatusInfoChangedEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information changes.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information changed events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/things/{thingUID}/statuschanged")

class InboxEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the InboxEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def InboxAddedEvent(self, thingUID: str = "*"):
        """
        Get events for added things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of added inbox events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/added")

    def InboxRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed inbox events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/removed")

    def InboxUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated inbox events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/inbox/{thingUID}/updated")

class LinkEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the LinkEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ItemChannelLinkAddedEvent(self, itemName: str = "*", channelUID: str = "*"):
        """
        Get events for added item-channel links.

        :param itemName: The name of the item (default is "*").
        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of added item-channel link events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/added")

    def ItemChannelLinkRemovedEvent(self, itemName: str = "*", channelUID: str = "*"):
        """
        Get events for removed item-channel links.

        :param itemName: The name of the item (default is "*").
        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of removed item-channel link events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/removed")

class ChannelEvents:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the ChannelEvents class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def ChannelDescriptionChangedEvent(self, channelUID: str = "*"):
        """
        Get events for changes in channel descriptions.

        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of channel description changed events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/descriptionchanged")

    def ChannelTriggeredEvent(self, channelUID: str = "*"):
        """
        Get events for triggered channels.

        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of channel triggered events.
        """
        return self.client._OpenHABClient__executeSSE(self.client.url + f"/rest/events?topics=openhab/channels/{channelUID}/triggered")
