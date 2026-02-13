from .AsyncClient import AsyncOpenHABClient
import aiohttp
import json


class AsyncEvents:
    def __init__(self, client: AsyncOpenHABClient):
        """
        Initializes the AsyncEvents class with an AsyncOpenHABClient object.
        """
        self.client = client

    async def getEvents(self, topics: str = None):
        """
        Get all available events, optionally filtered by topic asynchronously.
        """
        url = f"/rest/events" + (f"?topics={topics}" if topics else "")
        try:
            response = await self.client.executeSSE(url)
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 400:
                return {"error": "Topic is empty or contains invalid characters."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def initiateStateTracker(self):
        """
        Initiates a new item state tracker connection asynchronously.
        """
        try:
            response = await self.client.executeSSE("/rest/events/states", headers={"Accept": "*/*"})
            return response
        except aiohttp.ClientResponseError as err:
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}

    async def updateSSEConnectionItems(self, connectionID: str, items: list):
        """
        Changes the list of items a SSE connection will receive state updates for asynchronously.
        """
        try:
            response = await self.client.post(
                f"/rest/events/states/{connectionID}",
                data=json.dumps(items),
                headers={"Content-Type": "application/json"}
            )
            return response
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return {"error": "Unknown connectionID."}
            return {"error": f"HTTP error {err.status}: {err.message}"}
        except aiohttp.ClientError as err:
            return {"error": f"Request error: {str(err)}"}


class AsyncItemEvents:
    def __init__(self, client: AsyncOpenHABClient):
        self.client = client

    async def ItemEvent(self):
        return await self.client.executeSSE("/rest/events?topics=openhab/items")

    async def ItemAddedEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/added")

    async def ItemRemovedEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/removed")

    async def ItemUpdatedEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/updated")

    async def ItemCommandEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/command")

    async def ItemStateEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/state")

    async def ItemStatePredictedEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/statepredicted")

    async def ItemStateChangedEvent(self, itemName: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/statechanged")

    async def GroupItemStateChangedEvent(self, itemName: str, memberName: str):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/items/{itemName}/{memberName}/statechanged")


class AsyncThingEvents:
    def __init__(self, client: AsyncOpenHABClient):
        self.client = client

    async def ThingAddedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/things/{thingUID}/added")

    async def ThingRemovedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/things/{thingUID}/removed")

    async def ThingUpdatedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/things/{thingUID}/updated")

    async def ThingStatusInfoEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/things/{thingUID}/status")

    async def ThingStatusInfoChangedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/things/{thingUID}/statuschanged")


class AsyncInboxEvents:
    def __init__(self, client: AsyncOpenHABClient):
        self.client = client

    async def InboxAddedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/inbox/{thingUID}/added")

    async def InboxRemovedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/inbox/{thingUID}/removed")

    async def InboxUpdatedEvent(self, thingUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/inbox/{thingUID}/updated")


class AsyncLinkEvents:
    def __init__(self, client: AsyncOpenHABClient):
        self.client = client

    async def ItemChannelLinkAddedEvent(self, itemName: str = "*", channelUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/added")

    async def ItemChannelLinkRemovedEvent(self, itemName: str = "*", channelUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/links/{itemName}-{channelUID}/removed")


class AsyncChannelEvents:
    def __init__(self, client: AsyncOpenHABClient):
        self.client = client

    async def ChannelDescriptionChangedEvent(self, channelUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/channels/{channelUID}/descriptionchanged")

    async def ChannelTriggeredEvent(self, channelUID: str = "*"):
        return await self.client.executeSSE(f"/rest/events?topics=openhab/channels/{channelUID}/triggered")
