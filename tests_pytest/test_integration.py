"""
Integration tests against a real openHAB (set OPENHAB_TEST_URL and OPENHAB_TEST_TOKEN).

The tests only touch objects they create themselves (prefix PyTest).
"""
import asyncio
import json
import os
import threading
import time

import pytest

from openhab import (Actions, AsyncItemEvents, AsyncItems, AsyncOpenHABClient, AsyncRules, AsyncThings, Events,
                     ItemEvents, Items, Links, iterSSEEvents, Persistence, Rules, Sitemaps, Systeminfo, Tags, Things, Transformations)

ITEM = "PyTest_Switch"
NUMBER = "PyTest_Number"
RULE = "pytest_rule"
THING = "astro:moon:pytest"


@pytest.fixture(scope="module")
def items(client):
    api = Items(client)
    api.addOrUpdateItem(ITEM, {"type": "Switch", "name": ITEM, "label": "PyTest Switch"})
    api.addOrUpdateItem(NUMBER, {"type": "Number:Temperature", "name": NUMBER, "label": "PyTest Number"})
    yield api
    api.deleteItem(ITEM)
    api.deleteItem(NUMBER)


def test_systeminfo(client):
    assert "systemInfo" in Systeminfo(client).getSystemInfo()


def test_item_crud(items):
    assert items.getItem(ITEM)["label"] == "PyTest Switch"
    assert items.addTag(ITEM, "Light") == {"message": "OK"}
    assert "Light" in items.getItem(ITEM)["tags"]
    assert items.removeTag(ITEM, "Light") == {"message": "OK"}
    assert items.addMetadata(ITEM, "autoupdate", {"value": "true"})["message"] in ("Created.", "OK")
    assert "autoupdate" in items.getMetadataNamespaces(ITEM)
    assert items.removeMetadata(ITEM, "autoupdate") == {"message": "OK"}
    assert items.getItem("PyTest_DoesNotExist") == {"error": "Item not found."}


def test_command_and_state(items):
    assert items.sendCommand(ITEM, "ON") == {"message": "OK"}
    time.sleep(0.5)
    assert items.getItemState(ITEM) == "ON"
    assert items.postUpdate(NUMBER, "21.5 °C") == {"message": "Accepted."}
    assert items.getItemState(NUMBER) == "21.5 °C"
    assert "error" in items.sendCommand(ITEM, "HALF")
    assert "error" in items.postUpdate(ITEM, "HALF")


def test_sse_with_token(client, items):
    stream = ItemEvents(client).ItemStateChangedEvent(ITEM)
    assert not isinstance(stream, dict), stream
    received = []

    def toggle():
        time.sleep(0.5)
        items.sendCommand(ITEM, "OFF" if items.getItemState(ITEM) == "ON" else "ON")

    threading.Thread(target=toggle, daemon=True).start()
    started = time.time()
    with stream:
        for event in iterSSEEvents(stream):
            received.append(event["topic"])
            break
    assert time.time() - started < 3, "event arrived late"
    assert received == [f"openhab/items/{ITEM}/statechanged"]


def test_item_event_stream_opens(client):
    stream = ItemEvents(client).ItemEvent()
    assert stream.status_code == 200
    stream.close()
    filtered = Events(client).getEvents("openhab/items/*/statechanged,openhab/things/*/statuschanged")
    assert filtered.status_code == 200
    filtered.close()


def test_rule_lifecycle(client, items):
    rules = Rules(client)
    rules.deleteRule(RULE)
    rule = {"uid": RULE, "name": "PyTest", "triggers": [], "conditions": [],
            "actions": [{"id": "1", "type": "core.ItemCommandAction",
                         "configuration": {"itemName": ITEM, "command": "OFF"}}]}
    assert rules.createRule(rule)["message"] == "Rule successfully created."
    assert rules.getRule(RULE)["status"]["status"] in ("IDLE", "UNINITIALIZED", "INITIALIZING")
    items.sendCommand(ITEM, "ON")
    assert rules.runNow(RULE) == {"message": "OK"}
    time.sleep(0.5)
    assert items.getItemState(ITEM) == "OFF"
    assert rules.disable(RULE) == {"message": "OK"}
    assert rules.getRule(RULE)["status"]["statusDetail"] == "DISABLED"
    assert rules.enable(RULE) == {"message": "OK"}
    assert rules.deleteRule(RULE) == {"message": "OK"}


def test_thing_lifecycle(client):
    things = Things(client)
    things.deleteThing(THING)
    created = things.createThing({"UID": THING, "thingTypeUID": "astro:moon", "label": "PyTest Mond",
                                  "configuration": {"geolocation": "48.0,8.6"}})
    if isinstance(created, dict) and "error" in created:
        pytest.skip("astro binding not installed")
    time.sleep(1)
    assert things.getThingStatus(THING)["status"] in ("ONLINE", "INITIALIZING", "UNKNOWN")
    assert things.disableThing(THING)["UID"] == THING
    assert things.enableThing(THING)["UID"] == THING
    actions = Actions(client).getActions(THING)
    assert isinstance(actions, list)
    elevation = [a for a in actions if "getElevation" in a["actionUid"]]
    if elevation:
        assert "result" in Actions(client).executeAction(THING, elevation[0]["actionUid"], {})
    things.deleteThing(THING)


def test_links(client, items):
    channel = "astro:moon:pytest:position#elevation"
    things = Things(client)
    if "error" in things.createThing({"UID": THING, "thingTypeUID": "astro:moon", "label": "PyTest Mond",
                                      "configuration": {"geolocation": "48.0,8.6"}}):
        pytest.skip("astro binding not installed")
    links = Links(client)
    try:
        assert links.linkItemToChannel(NUMBER, channel, {}) == {"message": "OK"}
        assert links.getLink(NUMBER, channel)["channelUID"] == channel
        assert links.unlinkItemFromChannel(NUMBER, channel) == {"message": "OK"}
        assert links.getLink(NUMBER, channel) == {"error": "Link not found."}
    finally:
        things.deleteThing(THING)


def test_persistence_parameters(client, items):
    persistence = Persistence(client)
    services = {s["id"]: s for s in persistence.getServices()}
    modifiable = [sid for sid, s in services.items() if s.get("type") == "Modifiable"]
    if not modifiable:
        pytest.skip("no modifiable persistence service (e.g. inmemory) installed")
    sid = modifiable[0]
    assert persistence.storeItemData(NUMBER, "2026-01-01T10:00:00.000Z", "17.0", sid) == {"message": "OK"}
    data = persistence.getItemPersistenceData(NUMBER, sid, "2026-01-01T00:00:00.000Z", "2026-01-02T00:00:00.000Z")
    assert [p["state"] for p in data["data"]] == ["17.0"]
    assert persistence.deleteItemData(NUMBER, "2026-01-01T00:00:00.000Z", "2026-01-02T00:00:00.000Z", sid) \
        == {"message": "OK"}


def test_tags_and_transformations(client):
    tags = Tags(client)
    tags.deleteTag("Location_PyTest")
    assert tags.createTag({"uid": "Location_PyTest", "label": "PyTest", "description": "", "synonyms": []})["uid"] \
        == "Location_PyTest"
    assert tags.deleteTag("Location_PyTest")["message"].startswith("OK")
    tr = Transformations(client)
    assert tr.updateTransformation("config:map:pytest", {"uid": "config:map:pytest", "label": "PyTest", "type": "map",
                                                         "configuration": {"function": "ON=an"}}) == {"message": "OK"}
    assert tr.deleteTransformation("config:map:pytest") == {"message": "OK"}


def test_sitemap_subscription(client):
    result = Sitemaps(client).subscribeToSitemapEvents()
    assert result["subscriptionID"]


def test_async_variants(client, items):
    url, token = client.url, os.environ["OPENHAB_TEST_TOKEN"]

    async def run():
        async with AsyncOpenHABClient(url, token=token) as c:
            aitems = AsyncItems(c)
            assert await aitems.sendCommand(ITEM, "OFF") == {"message": "OK"}
            assert await aitems.getItem("PyTest_DoesNotExist") == {"error": "Item not found."}
            assert (await AsyncRules(c).getRules()) is not None
            stream = await AsyncItemEvents(c).ItemStateChangedEvent(ITEM)
            assert not isinstance(stream, dict), stream

            async def toggle():
                await asyncio.sleep(0.5)
                await aitems.sendCommand(ITEM, "ON")

            task = asyncio.create_task(toggle())
            topic = None
            async for line in stream.content:
                if line.startswith(b"data:"):
                    event = json.loads(line[5:])
                    if "topic" in event:
                        topic = event["topic"]
                        break
            stream.close()
            await task
            assert topic == f"openhab/items/{ITEM}/statechanged"
            status = await AsyncThings(c).getThings()
            assert isinstance(status, list)

    asyncio.run(asyncio.wait_for(run(), 20))


def test_module_config_param_is_plain_text(client, items):
    rules = Rules(client)
    rules.deleteRule(RULE)
    rules.createRule({"uid": RULE, "name": "PyTest", "triggers": [], "conditions": [],
                      "actions": [{"id": "1", "type": "core.ItemCommandAction",
                                   "configuration": {"itemName": ITEM, "command": "OFF"}}]})
    try:
        assert rules.setModuleConfigParam(RULE, "actions", "1", "command", "ON") == {"message": "OK"}
        assert rules.getModuleConfigParam(RULE, "actions", "1", "command") == "ON"
        assert rules.getRule(RULE)["actions"][0]["configuration"]["command"] == "ON"
    finally:
        rules.deleteRule(RULE)


def test_delete_all_links_returns_count(client, items):
    assert Links(client).deleteAllLinks(NUMBER) == {"count": 0}


def test_sitemap_event_stream(client, items):
    from openhab import UI, iterSSELines, parseSSEData
    ui, sitemaps = UI(client), Sitemaps(client)
    ui.deleteUIComponent("system:sitemap", "pytest_sitemap")
    ui.addUIComponent("system:sitemap", {"uid": "pytest_sitemap", "component": "Sitemap",
                                         "config": {"label": "PyTest"},
                                         "slots": {"widgets": [{"component": "Switch",
                                                                "config": {"item": ITEM}}]}})
    try:
        sub = sitemaps.subscribeToSitemapEvents()["subscriptionID"]
        sitemaps.getSitemapPage("pytest_sitemap", "pytest_sitemap", subscriptionID=sub)
        items.sendCommand(ITEM, "OFF")
        time.sleep(0.3)
        threading.Timer(1, lambda: items.sendCommand(ITEM, "ON")).start()
        stream = sitemaps.getSitemapEvents(sub, "pytest_sitemap", "pytest_sitemap")
        with stream:
            for line in iterSSELines(stream):
                event = parseSSEData(line)
                if event and event.get("widgetId"):
                    assert event["item"]["name"] == ITEM
                    break
    finally:
        ui.deleteUIComponent("system:sitemap", "pytest_sitemap")


def test_interpreter_answer_is_kept(client):
    from openhab import Voice
    answer = Voice(client).interpretTextBatch("xyzzy plugh", ["system"], language="de")
    assert "error" in answer and "(" in answer["error"]
