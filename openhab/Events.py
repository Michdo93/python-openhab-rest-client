from .Client import OpenHABClient, StatusResponse
import json
import requests


def _openStream(client: OpenHABClient, topics: str = None, path: str = "/rest/events", headers: dict = None,
                errors: dict = None):
    """
    Opens an SSE stream and translates HTTP errors into the error dictionaries
    used throughout this library.

    :return: The streaming requests.Response (iterate with iter_lines()) or {"error": ...}.
    """
    errors = errors or {}
    try:
        return client.executeSSE(path, headers=headers, params={"topics": topics} if topics else None)
    except requests.exceptions.HTTPError as err:
        statusCode = err.response.status_code
        if statusCode in errors:
            return {"error": errors[statusCode]}
        return {"error": f"HTTP error {statusCode}: {str(err)}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error: {str(err)}"}


class Events:
    def __init__(self, client: OpenHABClient):
        """
        Initializes the Events class with an OpenHABClient object.

        :param client: An instance of OpenHABClient that is used for REST-API communication.
        """
        self.client = client

    def getEvents(self, topics: str = None):
        """
        Get all available events, optionally filtered by topic.

        :param topics: A comma-separated list of topics to filter the events by
                       (e.g. "openhab/items/*/statechanged,openhab/things/*/statuschanged").
                       The wildcard * also matches slashes.

        :return: A SSE stream of events (requests.Response) or {"error": ...}.
        """
        return _openStream(self.client, topics,
                           errors={400: "Topic is empty or contains invalid characters."})

    def initiateStateTracker(self):
        """
        Initiates a new item state tracker connection.

        The first event of the stream carries the connection ID, which is needed for
        updateSSEConnectionItems().

        :return: A SSE stream (requests.Response) or {"error": ...}.
        """
        return _openStream(self.client, path="/rest/events/states", headers={"Accept": "*/*"})

    def updateSSEConnectionItems(self, connectionID: str, items: list):
        """
        Changes the list of items a SSE connection will receive state updates for.

        :param connectionID: The ID of the existing connection.
        :param items: A list of item names to subscribe to for state updates.

        :return: A success message when the update is completed.
        """
        try:
            response = self.client.post(f"/events/states/{connectionID}", data=json.dumps(items),
                                        headers={"Content-Type": "application/json"})

            if isinstance(response, StatusResponse):
                statusCode = response["status"]
            else:
                return response

        except requests.exceptions.HTTPError as err:
            statusCode = err.response.status_code
            if statusCode == 404:
                return {"error": "Unknown connectionID."}
            return {"error": f"HTTP error {statusCode}: {str(err)}"}

        except requests.exceptions.RequestException as err:
            return {"error": f"Request error: {str(err)}"}

        if statusCode == 200:
            return {"message": "OK"}
        return {"error": f"Unexpected response: {statusCode}"}


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
        return _openStream(self.client, "openhab/items/*")

    def ItemAddedEvent(self, itemName: str = "*"):
        """
        Get events for added items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of added item events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/added")

    def ItemRemovedEvent(self, itemName: str = "*"):
        """
        Get events for removed items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of removed item events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/removed")

    def ItemUpdatedEvent(self, itemName: str = "*"):
        """
        Get events for updated items.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of updated item events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/updated")

    def ItemCommandEvent(self, itemName: str = "*"):
        """
        Get events for item commands.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item command events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/command")

    def ItemStateEvent(self, itemName: str = "*"):
        """
        Get events for item state updates.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/state")

    def ItemStatePredictedEvent(self, itemName: str = "*"):
        """
        Get events for predicted item state changes.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state predicted events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/statepredicted")

    def ItemStateChangedEvent(self, itemName: str = "*"):
        """
        Get events for item state changes.

        Note: with the default "*", state changes of group items are included as
        well, because their topic openhab/items/<group>/<member>/statechanged also
        matches the pattern.

        :param itemName: The name of the item (default is "*").

        :return: A SSE stream of item state changed events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/statechanged")

    def GroupItemStateChangedEvent(self, itemName: str = "*", memberName: str = "*"):
        """
        Get events for state changes of group items.

        :param itemName: The name of the group item (default is "*").
        :param memberName: The name of the group member that caused the change (default is "*").

        :return: A SSE stream of group item state changed events.
        """
        return _openStream(self.client, f"openhab/items/{itemName}/{memberName}/statechanged")


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
        return _openStream(self.client, f"openhab/things/{thingUID}/added")

    def ThingRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed thing events.
        """
        return _openStream(self.client, f"openhab/things/{thingUID}/removed")

    def ThingUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated thing events.
        """
        return _openStream(self.client, f"openhab/things/{thingUID}/updated")

    def ThingStatusInfoEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information events.
        """
        return _openStream(self.client, f"openhab/things/{thingUID}/status")

    def ThingStatusInfoChangedEvent(self, thingUID: str = "*"):
        """
        Get events for thing status information changes.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of thing status information changed events.
        """
        return _openStream(self.client, f"openhab/things/{thingUID}/statuschanged")


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
        return _openStream(self.client, f"openhab/inbox/{thingUID}/added")

    def InboxRemovedEvent(self, thingUID: str = "*"):
        """
        Get events for removed things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of removed inbox events.
        """
        return _openStream(self.client, f"openhab/inbox/{thingUID}/removed")

    def InboxUpdatedEvent(self, thingUID: str = "*"):
        """
        Get events for updated things in the inbox.

        :param thingUID: The UID of the thing (default is "*").

        :return: A SSE stream of updated inbox events.
        """
        return _openStream(self.client, f"openhab/inbox/{thingUID}/updated")


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
        return _openStream(self.client, f"openhab/links/{itemName}-{channelUID}/added")

    def ItemChannelLinkRemovedEvent(self, itemName: str = "*", channelUID: str = "*"):
        """
        Get events for removed item-channel links.

        :param itemName: The name of the item (default is "*").
        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of removed item-channel link events.
        """
        return _openStream(self.client, f"openhab/links/{itemName}-{channelUID}/removed")


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
        return _openStream(self.client, f"openhab/channels/{channelUID}/descriptionchanged")

    def ChannelTriggeredEvent(self, channelUID: str = "*"):
        """
        Get events for triggered channels.

        :param channelUID: The UID of the channel (default is "*").

        :return: A SSE stream of channel triggered events.
        """
        return _openStream(self.client, f"openhab/channels/{channelUID}/triggered")
