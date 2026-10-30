"""
Helpers for reading openHAB's Server-Sent Events streams.

Why not simply ``response.iter_lines()``? With its default chunk size, requests
only hands out a line once 512 bytes have arrived or the *next* chunk starts –
an event can then show up seconds late (often only with the next ALIVE message).
``iterSSELines`` returns every line as soon as it is complete.
"""
import json


def iterSSELines(response):
    """
    Yields the lines of a synchronous SSE stream (requests.Response) as str,
    each one as soon as it has arrived.
    """
    raw = response.raw
    raw.decode_content = True
    read = getattr(raw, "read1", None)
    buffer = b""
    while True:
        # read1 returns whatever has arrived (at least one byte) – no waiting for a full buffer
        chunk = read(65536) if read else raw.read(1)
        if not chunk:
            break
        buffer += chunk
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            yield line.rstrip(b"\r").decode("utf-8", errors="replace")
    if buffer:
        yield buffer.decode("utf-8", errors="replace")


def parseSSEData(line: str):
    """
    Decodes one ``data:`` line of the openHAB event stream.

    :return: The event as dict with the payload already decoded (JSON in JSON),
             the raw dict for control messages such as ``{"type": "ALIVE"}``,
             or None for all other lines (``event:``, comments, empty lines).
    """
    if not line.startswith("data:"):
        return None
    try:
        event = json.loads(line[5:].strip())
    except ValueError:
        return None
    payload = event.get("payload")
    if isinstance(payload, str):
        try:
            event["payload"] = json.loads(payload)
        except ValueError:
            pass
    return event


def iterSSEEvents(response, includeAlive: bool = False):
    """
    Yields the events of a synchronous SSE stream as dicts with decoded payload.

    :param response: The stream returned by e.g. ItemEvents(client).ItemStateChangedEvent().
    :param includeAlive: Also yield ALIVE messages (default: False).
    """
    for line in iterSSELines(response):
        event = parseSSEData(line)
        if event is None:
            continue
        if "topic" in event or includeAlive:
            yield event


async def aiterSSELines(response):
    """Asynchronous counterpart of iterSSELines for an aiohttp.ClientResponse."""
    async for raw in response.content:
        yield raw.rstrip(b"\r\n").decode("utf-8", errors="replace")


async def aiterSSEEvents(response, includeAlive: bool = False):
    """Asynchronous counterpart of iterSSEEvents for an aiohttp.ClientResponse."""
    async for line in aiterSSELines(response):
        event = parseSSEData(line)
        if event is None:
            continue
        if "topic" in event or includeAlive:
            yield event
