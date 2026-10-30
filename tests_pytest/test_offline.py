"""Tests that run without openHAB."""
import ast
import inspect
import pathlib

import openhab
from openhab import AsyncOpenHABClient, OpenHABClient, StatusResponse

PKG = pathlib.Path(openhab.__file__).parent


def test_status_response_is_distinguishable():
    marker = StatusResponse(status=202)
    assert marker == {"status": 202} and marker.status == 202
    assert not isinstance({"status": "ONLINE"}, StatusResponse)


def test_build_url():
    c = OpenHABClient.__new__(OpenHABClient)
    c.url = "http://oh:8080"
    assert c._buildUrl("/items") == "http://oh:8080/rest/items"
    assert c._buildUrl("items") == "http://oh:8080/rest/items"
    assert c._buildUrl("/rest/items") == "http://oh:8080/rest/items"
    assert c._buildUrl("/rest/events?topics=a/#") == "http://oh:8080/rest/events?topics=a/#"
    assert c._buildUrl("/actions/t/astro.x#abc") == "http://oh:8080/rest/actions/t/astro.x%23abc"
    a = AsyncOpenHABClient("http://oh:8080/")
    assert a._buildUrl("/actions/t/x#1") == "http://oh:8080/rest/actions/t/x%231"


def test_clean_params():
    assert OpenHABClient._cleanParams({"a": None, "b": True, "c": 1}) == {"b": "true", "c": 1}
    assert AsyncOpenHABClient._cleanParams({"a": None, "b": False, "c": 1}) == {"b": "false", "c": "1"}


def _methods(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result = {}
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        for fn in cls.body:
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and not fn.name.startswith("_"):
                result[(cls.name.replace("Async", "", 1), fn.name)] = (
                    [a.arg for a in fn.args.args], isinstance(fn, ast.AsyncFunctionDef))
    return result


def test_async_classes_match_sync_classes():
    for path in sorted(PKG.glob("*.py")):
        if path.name.startswith("Async") or path.name in ("__init__.py", "Client.py", "SSE.py"):
            continue
        sync = _methods(path)
        asyn = _methods(PKG / f"Async{path.name}")
        assert sync.keys() == asyn.keys(), path.name
        for key in sync:
            assert sync[key][0] == asyn[key][0], key
            assert asyn[key][1], f"{key} must be async"


def test_everything_is_exported():
    for name in openhab.__all__:
        assert inspect.isclass(getattr(openhab, name)) or inspect.isfunction(getattr(openhab, name))


def test_sse_parsing():
    chunks = [b'event: message\ndata: {"topic":"openhab/items/A/statechanged",',
              b'"payload":"{\\"value\\":\\"ON\\"}","type":"ItemStateChangedEvent"}\n\n',
              b'event: alive\ndata: {"type":"ALIVE","interval":10}\n\n']

    class Raw:
        def __init__(self):
            self.parts = list(chunks)

        def read1(self, size):
            return self.parts.pop(0) if self.parts else b""

    class Fake:
        def __init__(self):
            self.raw = Raw()

    events = list(openhab.iterSSEEvents(Fake()))
    assert events == [{"topic": "openhab/items/A/statechanged", "payload": {"value": "ON"},
                       "type": "ItemStateChangedEvent"}]
    assert len(list(openhab.iterSSEEvents(Fake(), includeAlive=True))) == 2
