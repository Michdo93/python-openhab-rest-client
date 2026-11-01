# python-openhab-rest-client

A Python client for the openHAB REST API. This library enables easy interaction with the openHAB REST API to control smart home devices, retrieve status information, and process events.

## Features

Supports the following openHAB REST API endpoints:

- Actions
- Addons
- Audio
- Auth
- ChannelTypes
- ConfigDescriptions
- Discovery
- Events (ItemEvents, ThingEvents, InboxEvents, LinkEvents, ChannelEvents)
- Iconsets
- Inbox
- Items
- Links
- Logging
- ModuleTypes
- Persistence
- ProfileTypes
- Rules
- Services
- Sitemaps
- Systeminfo
- Tags
- Templates
- ThingTypes
- Things
- Transformations
- UI
- UUID
- Voice

All of the above are also available as asynchronous variants (e.g. `AsyncItems`, `AsyncThings`, etc.) using `AsyncOpenHABClient` based on `aiohttp`.

Supports both Server-Sent Events (SSE) and regular REST requests. SSE is used for the events of openHAB.

## Requirements

- Python 3.8 or newer
- `requests`
- `aiohttp`

Tested against openHAB 5.2.3 (Java 21). The library also works with openHAB 4.x;
parameters that were added in later openHAB versions (e.g. `source`, `parents`,
`displayState`) are only sent if you pass them.

## Installation

Install via pip:

```sh
pip install python-openhab-rest-client
```

Here is the complete section translated into English, formatted to match your README:

---

### Secure HTTPS & Self-Signed Certificates (TLS)

When running openHAB over HTTPS with a custom or self-signed certificate, you must ensure that Python (via the underlying `requests` library) trusts the certificate and successfully validates the hostname.

#### 1. Switch openHAB to HTTPS

1. **Disable HTTP:**
Open the configuration file `/etc/openhab/services/org.ops4j.pax.web.cfg` (if it is not existing, create it) and set:
```properties
org.osgi.service.http.enabled=false
org.osgi.service.http.secure.enabled=true
org.ops4j.pax.web.ssl.port=8443
```

It could also help to edit the `/etc/default/openhab` file and make this changes:

```
#########################
## PORTS
## The ports openHAB will bind its HTTP/HTTPS web server to.

#OPENHAB_HTTP_PORT=8080
OPENHAB_HTTPS_PORT=8443
```

This ensures openHAB runs exclusively on the secure HTTPS port (default `8443`).
2. **Generate Keystore with a Proper SAN (Subject Alternative Name):**
Modern OpenSSL and Python versions strictly require a SAN entry in the certificate to prevent hostname mismatches. Create a new keystore using Java's `keytool` (replace `<your-hostname>` with your actual hostname):
```bash
sudo rm /var/lib/openhab/etc/keystore
sudo keytool -genkeypair -alias openhab -keyalg RSA -keysize 2048 -validity 365 \
  -keystore /var/lib/openhab/etc/keystore -storepass openhab -keypass openhab \
  -dname "CN=openhab" -ext "san=dns:<your-hostname>,ip:127.0.0.1,dns:localhost"
sudo chown openhab:openhab /var/lib/openhab/etc/keystore
sudo systemctl restart openhab
```

3. **Export the Certificate in PEM Format:**
Export the public certificate so your Python client can read and trust it:
```bash
sudo keytool -exportcert -rfc -alias openhab -keystore /var/lib/openhab/etc/keystore \
  -storepass openhab -file /home/$USER/openhab-exported.crt
sudo chown $USER:$USER /home/$USER/openhab-exported.crt
```

#### 2. Usage in the Python Client

Since self-signed certificates are rejected by default, you can pass the absolute path to the exported `.crt` file via the `verify` parameter of the client. The library will cryptographically verify the connection against your certificate:

```python
from openhab import OpenHABClient, Items

client = OpenHABClient(
    url="https://<your-hostname>:8443", 
    username="openhab", 
    password="habopen", 
    verify="/home/smarthome/openhab-exported.crt"
)

itemsAPI = Items(client)
allItems = itemsAPI.getItems()
print("All Items:", allItems)
```

*(Note: For the asynchronous client `AsyncOpenHABClient`, the `verify` parameter works the exact same way via `aiohttp`.)*

## Usage

Basically, you always need the `OpenHABClient` (or `AsyncOpenHABClient` for async usage). Regardless of whether you carry out a normal `REST request` or one via `SSE`.

### Authentication

#### Basic Authentication

```python
from openhab import OpenHABClient

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
```

The `url`, the `username` and the `password` can also vary. In particular, it is possible that `url` could be a remote IP address or even the openHAB cloud.

#### Token-based Authentication

It is also conceivable that a `token` could be used instead of `basic authentication`, i.e. with a `username` and `password`. A `token` is used by default in openHAB. The `basic authentication` must actually be activated manually.

For token-based access, the initialization of the client is as follows:

```python
client = OpenHABClient(url="http://127.0.0.1:8080", token="oh.openhab.U0doM1Lz4kJ6tPlVGjH17jjm4ZcTHIHi7sMwESzrIybKbCGySmBMtysPnObQLuLf7PgqnI7jWQ5LosySY8Q")
```

Of course, your `token` will probably look different here too.

### Requests

#### Normal REST requests

Depending on the `endpoint`, a corresponding class must be imported from the library. If you want to access endpoints of the REST API with which you want to access `items`, you import the `Items` class, for example. There are then different functions in this class for each endpoint for items. More details can be found in the documentation.

An easy example could be:

```python
from openhab import OpenHABClient, Items

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemsAPI = Items(client)

allItems = itemsAPI.getItems()
print("All Items:", allItems)
```

#### Async REST requests

All synchronous classes have an async counterpart that uses `AsyncOpenHABClient` and `aiohttp`. The `AsyncOpenHABClient` must be used as an async context manager with `async with`.

```python
import asyncio
from openhab import AsyncOpenHABClient, AsyncItems

async def main():
    async with AsyncOpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen") as client:
        itemsAPI = AsyncItems(client)
        allItems = await itemsAPI.getItems()
        print("All Items:", allItems)

asyncio.run(main())
```

#### Return values and errors

All methods follow the same conventions – in the synchronous and in the asynchronous classes:

| Situation | Return value |
|---|---|
| openHAB answers with JSON | the decoded JSON (`dict` or `list`) |
| openHAB answers with plain text (e.g. `getItemState`) | `str` |
| openHAB answers without a body (e.g. `sendCommand`) | `{"message": "..."}` |
| openHAB rejects the request (4xx/5xx) | `{"error": "..."}` – including openHAB's own error message if it sent one |
| network error, timeout | `{"error": "Request error: ..."}` |

So you can always check for errors like this:

```python
result = itemsAPI.sendCommand("Livingroom_Light", "ON")
if isinstance(result, dict) and "error" in result:
    print("openHAB rejected the command:", result["error"])
```

The low-level methods `client.get/post/put/delete` return the JSON, the text or – for
responses without a body – a `StatusResponse` (a `dict` like `{"status": 202}`, with
`"location"` if openHAB sent a `Location` header). They raise
`requests.exceptions.HTTPError` (sync) or `aiohttp.ClientResponseError` (async) for
4xx/5xx responses.

#### Server-sent Events (SSE) requests

All normal REST requests are static. This means that they do not react to status changes. You would therefore have to send several REST requests in succession (polling). Or you can use the various events from openHAB. This can be done using server-sent events (SSE) without polling. The server sends a message to the client exactly when it can make something available. With polling, on the other hand, you would have to constantly send requests to the server, which would significantly increase the network and server load.

There are various [events](https://www.openhab.org/docs/developer/utils/events.html) in openHAB. For `ItemEvents`, `ThingEvents`, `InboxEvents`, `LinkEvents` and `ChannelEvents` there are own classes. However, there is also the `Events` class. More information can be found in the documentation.

An example looks like this:

```python
from openhab import OpenHABClient, ItemEvents

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemEvents = ItemEvents(client)

response = itemEvents.ItemStateChangedEvent()

with response as events:
    for line in events.iter_lines():
        line = line.decode()

        if "data" in line:
            line = line.replace("data: ", "")

            try:
                data = json.loads(line)
                print(data)
            except json.decoder.JSONDecodeError:
                print("Event could not be converted to JSON")
```

**Tip:** use the helpers `iterSSEEvents(response)` / `iterSSELines(response)` (and
`aiterSSEEvents` / `aiterSSELines` for the async client). `response.iter_lines()` with its
default arguments may hand out an event only when the *next* data arrives, i.e. seconds
late. `iterSSEEvents` also decodes the payload:

```python
from openhab import OpenHABClient, ItemEvents, iterSSEEvents

client = OpenHABClient(url="http://127.0.0.1:8080", token="oh.openhab...")
with ItemEvents(client).ItemStateChangedEvent() as stream:
    for event in iterSSEEvents(stream):
        print(event["topic"], event["payload"]["value"])
```

Remember that the `payload` of every event is itself a JSON string and has to be
decoded a second time. openHAB also sends `{"type": "ALIVE", ...}` messages every few
seconds – they have no `topic` and can be used as a heartbeat. The wildcard `*` in a
topic also matches slashes, so `openhab/items/*/statechanged` includes the state
changes of group items (`openhab/items/<group>/<member>/statechanged`).

The SSE stream uses the session of the client, i.e. token and Basic Authentication
are sent as well. If openHAB rejects the stream (e.g. `401`), the event methods return
`{"error": ...}` instead of a stream.

Asynchronous variant:

```python
import asyncio, json
from openhab import AsyncOpenHABClient, AsyncItemEvents

async def main():
    async with AsyncOpenHABClient(url="http://127.0.0.1:8080", token="oh.openhab...") as client:
        response = await AsyncItemEvents(client).ItemStateChangedEvent("Livingroom_Light")
        async for line in response.content:
            line = line.decode().strip()
            if line.startswith("data:"):
                event = json.loads(line[5:])
                if "topic" in event:
                    print(event["topic"], json.loads(event["payload"]))
        response.close()

asyncio.run(main())
```

### Tests

There is also a test function for each function. This means that every class that you import also has a test class that you can import. These tests work with a try-catch, as well as with a print output. Neither the value of the REST API nor something like True or False is returned. Effectively, however, the actual function is called from this test function and also executed in full, unless an exception is thrown.

In other words... For example, if you use the following import,

```python
from openhab import Items
```

then the test class to be imported would be the following:

```python
from openhab.tests import ItemsTest
```

From e.g. the following function

```python
itemsAPI = Items(client)
itemsAPI.sendCommand("testSwitch", "ON")
```

then becomes the following function for the test:

```python
itemsTest = ItemsTest(client)
itemsTest.testSendCommand("testSwitch", "ON")
```

However, both would also really execute a sendCommand in openHAB. The test classes test whether a function can be executed. In the end, it can only not be executed if the endpoint does not exist or has been implemented incorrectly. However, a non-existent endpoint can also occur, for example, if the name of the item is incorrect.

### Automated tests (pytest)

`tests_pytest/` contains automated tests:

- `test_offline.py` runs without openHAB (URL building, `StatusResponse`, parity between
  the synchronous and the generated asynchronous classes).
- `test_integration.py` runs against a real openHAB instance. It is skipped unless
  `OPENHAB_TEST_URL` and `OPENHAB_TEST_TOKEN` (an API token of an administrator) are set.
  The tests create and delete their own items, rules, tags and things (all prefixed with
  `PyTest`) and only send commands to these test items.

```sh
pip install -e . pytest
pytest tests_pytest                        # offline tests only
OPENHAB_TEST_URL=http://127.0.0.1:8080 OPENHAB_TEST_TOKEN=oh.xxx pytest tests_pytest -v
```

### Development: synchronous and asynchronous classes

The synchronous classes in `openhab/*.py` are the single source of truth. The
asynchronous classes `openhab/Async*.py` are generated from them, so both always have
the same methods, parameters, return values and error messages:

```sh
python tools/generate_async.py
```

## Full list of Methods

---

### OpenHABClient

`OpenHABClient` is a Python class that provides an interface to interact with the openHAB REST API. It allows users to send requests to openHAB to retrieve and manipulate smart home devices, events, and configurations. The get, put, post and delete methods are used in the other classes for the client. You therefore do not need to use them raw.

#### Initialization

##### Constructor

```python
from openhab import OpenHABClient

OpenHABClient(url: str, username: str = None, password: str = None, token: str = None, timeout: float = 10, verify=True)
```

###### Parameters:
- `url` (str): The base URL of the openHAB server (e.g., "http://127.0.0.1:8080").
- `username` (str, optional): Username for Basic Authentication (default is `None`).
- `password` (str, optional): Password for Basic Authentication (default is `None`).
- `token` (str, optional): Bearer Token for Token-based Authentication (default is `None`).

###### Example:

```python
client = OpenHABClient("http://127.0.0.1:8080", username="admin", password="password")
```

#### Methods

##### `get`

```python
get(endpoint: str, headers: dict = None, params: dict = None)
```

Sends a GET request to the openHAB server.

###### Parameters:
- `endpoint` (str): The API endpoint (e.g., `"/items"`).
- `headers` (dict, optional): Headers to include in the request.
- `params` (dict, optional): Query parameters for the request.

###### Example:

```python
response = client.get("/items")
print(response)
```

##### `post`

```python
post(endpoint: str, headers: dict = None, data=None, params: dict = None)
```

Sends a POST request to the openHAB server.

###### Parameters:
- `endpoint` (str): The API endpoint (e.g., `"/items"`).
- `headers` (dict, optional): Headers to include in the request.
- `data` (optional): Data to send in the request body.
- `params` (dict, optional): Query parameters for the request.

###### Example:

```python
data = {"type": "Switch", "state": "ON"}
response = client.post("/items/light", data=json.dumps(data))
print(response)
```

##### `put`

```python
put(endpoint: str, headers: dict = None, data=None, params: dict = None)
```

Sends a PUT request to update a resource in openHAB.

###### Example:

```python
data = {"state": "OFF"}
response = client.put("/items/light", data=json.dumps(data))
print(response)
```

##### `delete`

```python
delete(endpoint: str, headers: dict = None, data=None, params: dict = None)
```

Sends a DELETE request to remove a resource from openHAB.

###### Example:

```python
response = client.delete("/items/light")
print(response)
```

#### Authentication

The client supports two types of authentication:

- **Basic Authentication** (Username & Password)
- **Bearer Token Authentication**

If a token is provided, it is used for authentication; otherwise, Basic Authentication is used if credentials are supplied.

#### Error Handling

Errors during requests are caught and logged, with appropriate exception handling for HTTP errors, connection issues, and timeouts.

---

### AsyncOpenHABClient

`AsyncOpenHABClient` is the asynchronous counterpart to `OpenHABClient`. It uses `aiohttp` and must be used as an async context manager with `async with`. All async API classes require an `AsyncOpenHABClient` instance.

#### Initialization

##### Constructor

```python
from openhab import AsyncOpenHABClient

AsyncOpenHABClient(url: str, username: str = None, password: str = None, token: str = None, timeout: float = 10, verify: bool = True)
```

###### Parameters:
- `url` (str): The base URL of the openHAB server.
- `username` (str, optional): Username for Basic Authentication.
- `password` (str, optional): Password for Basic Authentication.
- `token` (str, optional): Bearer Token for Token-based Authentication.

#### Usage

`AsyncOpenHABClient` must always be used as an async context manager. It opens and closes the underlying `aiohttp.ClientSession` automatically.

```python
import asyncio
from openhab import AsyncOpenHABClient, AsyncItems

async def main():
    async with AsyncOpenHABClient(url="http://127.0.0.1:8080", token="oh.openhab...") as client:
        itemsAPI = AsyncItems(client)
        items = await itemsAPI.getItems()
        print(items)

asyncio.run(main())
```

#### Methods

The async client exposes the same HTTP primitives as the sync client, but as coroutines:

- `async get(endpoint, headers, params)`
- `async post(endpoint, headers, data, params)`
- `async put(endpoint, headers, data, params)`
- `async delete(endpoint, headers, data, params)`

---

### Actions

The `Actions` class provides methods to interact with the openHAB actions API. It allows retrieving available actions for a specific `thingUID` and executing actions.

#### Initialization

```python
from openhab import OpenHABClient, Actions

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
actions = Actions(client)
```

#### Methods

##### `getActions(thingUID: str, language: str = None) -> list`

Retrieves all available actions for a given thing UID.

**Parameters:**
- `thingUID` (str): The UID of the thing for which actions should be retrieved.
- `language` (str, optional): The language for the response (`Accept-Language` header).

**Returns:** A list of available actions.

###### Example:

```python
actions_list = actions.getActions("myThingUID")
print(actions_list)
```

##### `executeAction(thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str`

Executes an action on a specific thing.

**Parameters:**
- `thingUID` (str): The UID of the thing on which the action is executed.
- `actionUID` (str): The UID of the action to be performed.
- `actionInputs` (dict): A dictionary containing input parameters for the action.
- `language` (str, optional): The language for the response.

**Returns:** The response from the openHAB server.

###### Example:

```python
response = actions.executeAction("myThingUID", "actionID", {"param1": "value1"})
print(response)
```

---

### AsyncActions

The `AsyncActions` class is the asynchronous counterpart to `Actions`. It requires an `AsyncOpenHABClient`.

#### Methods

##### `async getActions(thingUID: str, language: str = None) -> list`

Asynchronously retrieves all available actions for a given thing UID.

##### `async executeAction(thingUID: str, actionUID: str, actionInputs: dict, language: str = None) -> str`

Asynchronously executes an action on a specific thing.

###### Example:

```python
async with AsyncOpenHABClient(url="http://127.0.0.1:8080", token="...") as client:
    asyncActions = AsyncActions(client)
    result = await asyncActions.executeAction("myThingUID", "actionID", {"param1": "value1"})
    print(result)
```

---

### Addons

The `Addons` class provides methods for interacting with the openHAB add-ons via the REST API.

#### Methods

##### `getAddons(serviceID: str = None, language: str = None) -> dict`

Retrieves a list of all available add-ons.

**Parameters:**
- `serviceID` (str, optional): Filter by service ID.
- `language` (str, optional): Language preference for the response.

**Returns:** A dictionary containing add-ons data.

##### `getAddon(addonID: str, serviceID: str = None, language: str = None) -> dict`

Retrieves details of a specific add-on by its ID.

**Parameters:**
- `addonID` (str): The unique identifier of the add-on.
- `serviceID` (str, optional): Filter by service ID.
- `language` (str, optional): Language preference for the response.

**Returns:** A dictionary containing details of the specified add-on.

##### `getAddonConfig(addonID: str, serviceID: str = None) -> dict`

Retrieves the configuration of a specific add-on.

**Parameters:**
- `addonID` (str): The unique identifier of the add-on.
- `serviceID` (str, optional): Filter by service ID.

**Returns:** A dictionary containing the configuration of the add-on.

##### `updateAddonConfig(addonID: str, configData: dict, serviceID: str = None) -> dict`

Updates the configuration of a specific add-on.

**Parameters:**
- `addonID` (str): The unique identifier of the add-on.
- `configData` (dict): Dictionary containing new configuration settings.
- `serviceID` (str, optional): Specify the target service.

**Returns:** A dictionary containing the updated configuration.

##### `installAddon(addonID: str, serviceID: str = None) -> dict`

Installs an add-on by its ID.

**Parameters:**
- `addonID` (str): The unique identifier of the add-on.
- `serviceID` (str, optional): Specify the target service.

**Returns:** A dictionary containing the installation status.

##### `uninstallAddon(addonID: str, serviceID: str = None) -> dict`

Uninstalls an add-on by its ID.

**Parameters:**
- `addonID` (str): The unique identifier of the add-on.
- `serviceID` (str, optional): Specify the target service.

**Returns:** A dictionary containing the uninstallation status.

##### `getAddonServices(language: str = None) -> dict`

Retrieves a list of all available add-on services.

**Parameters:**
- `language` (str, optional): Language preference for the response.

**Returns:** A dictionary containing available add-on services.

##### `getAddonSuggestions(language: str = None) -> dict`

Retrieves a list of suggested add-ons for installation.

**Parameters:**
- `language` (str, optional): Language preference for the response.

**Returns:** A dictionary containing suggested add-ons.

##### `getAddonTypes(serviceID: str = None, language: str = None) -> dict`

Retrieves a list of all available add-on types.

**Parameters:**
- `serviceID` (str, optional): Filter by service ID.
- `language` (str, optional): Language preference for the response.

**Returns:** A dictionary containing available add-on types.

##### `installAddonFromUrl(url: str) -> dict`

Installs an add-on from a given URL.

**Parameters:**
- `url` (str): The URL of the add-on to install.

**Returns:** A dictionary containing the installation status.

---

### AsyncAddons

The `AsyncAddons` class is the asynchronous counterpart to `Addons`. It provides the same methods as `Addons`, each as a coroutine prefixed with `async`:

- `async getAddons(serviceID, language)`
- `async getAddon(addonID, serviceID, language)`
- `async getAddonConfig(addonID, serviceID)`
- `async updateAddonConfig(addonID, configData, serviceID)`
- `async installAddon(addonID, serviceID)`
- `async uninstallAddon(addonID, serviceID)`
- `async getAddonServices(language)`
- `async getAddonSuggestions(language)`
- `async getAddonTypes(serviceID, language)`
- `async installAddonFromUrl(url)`

---

### Audio

The `Audio` class provides methods for interacting with the openHAB audio API. It allows retrieving default audio sinks and sources, as well as listing all available sinks and sources.

#### Initialization

```python
from openhab import OpenHABClient, Audio

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
audio = Audio(client)
```

#### Methods

##### `getDefaultSink(language: str = None) -> dict`

Retrieves the default audio sink.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** Information about the default sink.

##### `getDefaultSource(language: str = None) -> dict`

Retrieves the default audio source.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** Information about the default source.

##### `getSinks(language: str = None) -> list`

Retrieves a list of all available audio sinks.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of available audio sinks.

##### `getSources(language: str = None) -> list`

Retrieves a list of all available audio sources.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of available audio sources.

---

### AsyncAudio

The `AsyncAudio` class is the asynchronous counterpart to `Audio`. It provides the same methods as coroutines:

- `async getDefaultSink(language)`
- `async getDefaultSource(language)`
- `async getSinks(language)`
- `async getSources(language)`

---

### Auth

The `Auth` class provides methods for handling authentication in openHAB, including retrieving API tokens, revoking tokens, logging out, and managing authentication sessions.

#### Initialization

```python
from openhab import OpenHABClient, Auth

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
auth = Auth(client)
```

#### Methods

##### `getAPITokens() -> dict`

Retrieves the API tokens associated with the authenticated user.

**Returns:** JSON response containing API tokens.

##### `revokeAPIToken(tokenName: str) -> dict`

Revokes a specific API token.

**Parameters:**
- `tokenName` (str): The name of the API token to revoke.

**Returns:** JSON response confirming the revocation.

##### `logout(refreshToken: str, sessionID: str) -> dict`

Terminates the session associated with a given refresh token.

**Parameters:**
- `refreshToken` (str): The refresh token used to delete the session.
- `sessionID` (str): The session ID associated with the refresh token.

**Returns:** JSON response confirming the logout.

##### `getSessions() -> dict`

Retrieves the sessions associated with the authenticated user.

**Returns:** JSON response containing session details.

##### `getToken(useCookie: bool = False, grantType: str = None, code: str = None, redirectURI: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None) -> dict`

Obtains access and refresh tokens.

**Parameters:**
- `useCookie` (bool, optional): Whether to use cookies for the session (default `False`).
- `grantType` (str, optional): The type of grant being requested.
- `code` (str, optional): Authorization code for authentication.
- `redirectURI` (str, optional): Redirect URI for OAuth authentication.
- `clientID` (str, optional): Client ID for authentication.
- `refreshToken` (str, optional): Refresh token for token renewal.
- `codeVerifier` (str, optional): Code verifier for PKCE authentication.

**Returns:** JSON response containing access and refresh tokens.

---

### AsyncAuth

The `AsyncAuth` class is the asynchronous counterpart to `Auth`. It provides the same methods as coroutines:

- `async getAPITokens()`
- `async revokeAPIToken(tokenName)`
- `async logout(refreshToken, sessionID)`
- `async getSessions()`
- `async getToken(useCookie, grantType, code, redirectURI, clientID, refreshToken, codeVerifier)`

---

### ChannelTypes

The `ChannelTypes` class provides methods to interact with openHAB's channel types.

#### Initialization

```python
from openhab import OpenHABClient, ChannelTypes

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
channelTypes = ChannelTypes(client)
```

#### Methods

##### `getChannelTypes(prefixes: str = None, language: str = None) -> list`

Retrieves all available channel types.

**Parameters:**
- `prefixes` (str, optional): Filter channel types by prefix.
- `language` (str, optional): Language for the response.

**Returns:** A list of available channel types.

##### `getChannelType(channelTypeUID: str, language: str = None) -> dict`

Retrieves details of a specific channel type by its UID.

**Parameters:**
- `channelTypeUID` (str): The unique identifier of the channel type.
- `language` (str, optional): Language for the response.

**Returns:** JSON response containing details of the specified channel type.

##### `getLinkableItemTypes(channelTypeUID: str) -> list`

Retrieves the item types that can be linked to a specified trigger channel type.

**Parameters:**
- `channelTypeUID` (str): The unique identifier of the channel type.

**Returns:** A list of item types that can be linked to the given channel type.

---

### AsyncChannelTypes

The `AsyncChannelTypes` class is the asynchronous counterpart to `ChannelTypes`:

- `async getChannelTypes(prefixes, language)`
- `async getChannelType(channelTypeUID, language)`
- `async getLinkableItemTypes(channelTypeUID)`

---

### ConfigDescriptions

The `ConfigDescriptions` class provides methods to interact with openHAB's configuration descriptions.

#### Initialization

```python
from openhab import OpenHABClient, ConfigDescriptions

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
configDescriptions = ConfigDescriptions(client)
```

#### Methods

##### `getConfigDescriptions(scheme: str = None, language: str = None) -> list`

Retrieves all available configuration descriptions.

**Parameters:**
- `scheme` (str, optional): Filter results by a specific scheme.
- `language` (str, optional): Language for the response.

**Returns:** A list of available configuration descriptions.

##### `getConfigDescription(uri: str, language: str = None) -> dict`

Retrieves a specific configuration description by its URI.

**Parameters:**
- `uri` (str): The URI of the requested configuration description.
- `language` (str, optional): Language for the response.

**Returns:** JSON response containing details of the specified configuration description.

---

### AsyncConfigDescriptions

The `AsyncConfigDescriptions` class is the asynchronous counterpart to `ConfigDescriptions`:

- `async getConfigDescriptions(scheme, language)`
- `async getConfigDescription(uri, language)`

---

### Discovery

The `Discovery` class provides methods to interact with openHAB's discovery service.

#### Initialization

```python
from openhab import OpenHABClient, Discovery

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
discovery = Discovery(client)
```

#### Methods

##### `getDiscoveryBindings() -> list`

Retrieves all bindings that support discovery.

**Returns:** A list of strings representing the bindings that support discovery.

##### `getBindingInfo(bindingID: str, language: str = None) -> dict`

Retrieves information about a specific binding.

**Parameters:**
- `bindingID` (str): The ID of the binding.
- `language` (str, optional): Language for the response.

**Returns:** A dictionary containing the binding information.

##### `startBindingScan(bindingID: str, input: str = None) -> int`

Starts the asynchronous discovery process for a binding and returns the timeout duration in seconds.

**Parameters:**
- `bindingID` (str): The ID of the binding for which discovery is to be started.
- `input` (str, optional): Optional input for the scan.

**Returns:** Timeout duration of the discovery operation in seconds.

###### Example:

```python
timeout = discovery.startBindingScan("zwave")
print(timeout)
```

---

### AsyncDiscovery

The `AsyncDiscovery` class is the asynchronous counterpart to `Discovery`:

- `async getDiscoveryBindings()`
- `async getBindingInfo(bindingID, language)`
- `async startBindingScan(bindingID, input)`

---

### Events

The `Events` class provides methods to interact with openHAB's event service via SSE. It allows retrieving various event streams.

#### Initialization

```python
from openhab import OpenHABClient, Events

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
events = Events(client)
```

#### Methods

##### `getEvents(topics: str = None) -> list`

Retrieves a stream of all openHAB events, optionally filtered by topic.

**Parameters:**
- `topics` (str, optional): Comma-separated list of topics to filter events.

**Returns:** An SSE response stream.

##### `initiateStateTracker() -> str`

Initiates a new state tracker connection and returns the connection ID.

**Returns:** A string containing the SSE connection ID.

##### `updateSSEConnectionItems(connectionID: str, items: list) -> str`

Updates the items tracked by an existing SSE state tracker connection.

**Parameters:**
- `connectionID` (str): The ID of the SSE connection to update.
- `items` (list): A list of item names to track.

**Returns:** The response from the server.

---

### ItemEvents

The `ItemEvents` class provides SSE streams for item-related events.

#### Initialization

```python
from openhab import OpenHABClient, ItemEvents

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
itemEvents = ItemEvents(client)
```

#### Methods

##### `ItemEvent()`

Subscribes to all item events.

##### `ItemAddedEvent(itemName: str = "*")`

Subscribes to item added events.

**Parameters:**
- `itemName` (str, optional): The name of the item to filter by (default `"*"` for all items).

##### `ItemRemovedEvent(itemName: str = "*")`

Subscribes to item removed events.

##### `ItemUpdatedEvent(itemName: str = "*")`

Subscribes to item updated events.

##### `ItemCommandEvent(itemName: str = "*")`

Subscribes to item command events.

##### `ItemStateEvent(itemName: str = "*")`

Subscribes to item state events.

##### `ItemStatePredictedEvent(itemName: str = "*")`

Subscribes to item state predicted events.

##### `ItemStateChangedEvent(itemName: str = "*")`

Subscribes to item state changed events.

**Parameters:**
- `itemName` (str, optional): The name of the item to filter by (default `"*"` for all items).

**Returns:** An SSE response stream.

###### Example:

```python
response = itemEvents.ItemStateChangedEvent()

with response as events:
    for line in events.iter_lines():
        line = line.decode()
        if "data" in line:
            line = line.replace("data: ", "")
            try:
                data = json.loads(line)
                print(data)
            except json.decoder.JSONDecodeError:
                print("Event could not be decoded as JSON")
```

##### `GroupItemStateChangedEvent(itemName: str, memberName: str)`

Subscribes to group item state changed events for a specific member.

**Parameters:**
- `itemName` (str): The name of the group item.
- `memberName` (str): The name of the member item.

---

### ThingEvents

The `ThingEvents` class provides SSE streams for thing-related events.

#### Methods

##### `ThingAddedEvent(thingUID: str = "*")`

Subscribes to thing added events.

##### `ThingRemovedEvent(thingUID: str = "*")`

Subscribes to thing removed events.

##### `ThingUpdatedEvent(thingUID: str = "*")`

Subscribes to thing updated events.

##### `ThingStatusInfoEvent(thingUID: str = "*")`

Subscribes to thing status info events.

##### `ThingStatusInfoChangedEvent(thingUID: str = "*")`

Subscribes to thing status info changed events.

---

### InboxEvents

The `InboxEvents` class provides SSE streams for inbox-related events.

#### Methods

##### `InboxAddedEvent(thingUID: str = "*")`

Subscribes to inbox added events.

##### `InboxRemovedEvent(thingUID: str = "*")`

Subscribes to inbox removed events.

##### `InboxUpdatedEvent(thingUID: str = "*")`

Subscribes to inbox updated events.

---

### LinkEvents

The `LinkEvents` class provides SSE streams for link-related events.

#### Methods

##### `ItemChannelLinkAddedEvent(itemName: str = "*", channelUID: str = "*")`

Subscribes to item-channel link added events.

**Parameters:**
- `itemName` (str, optional): Filter by item name (default `"*"`).
- `channelUID` (str, optional): Filter by channel UID (default `"*"`).

##### `ItemChannelLinkRemovedEvent(itemName: str = "*", channelUID: str = "*")`

Subscribes to item-channel link removed events.

---

### ChannelEvents

The `ChannelEvents` class provides SSE streams for channel-related events.

#### Methods

##### `ChannelDescriptionChangedEvent(channelUID: str = "*")`

Subscribes to channel description changed events.

**Parameters:**
- `channelUID` (str, optional): Filter by channel UID (default `"*"`).

##### `ChannelTriggeredEvent(channelUID: str = "*")`

Subscribes to channel triggered events.

---

### AsyncEvents

The `AsyncEvents` class is the asynchronous counterpart to `Events`:

- `async getEvents(topics)`
- `async initiateStateTracker()`
- `async updateSSEConnectionItems(connectionID, items)`

### AsyncItemEvents

The `AsyncItemEvents` class is the asynchronous counterpart to `ItemEvents`:

- `async ItemEvent()`
- `async ItemAddedEvent(itemName)`
- `async ItemRemovedEvent(itemName)`
- `async ItemUpdatedEvent(itemName)`
- `async ItemCommandEvent(itemName)`
- `async ItemStateEvent(itemName)`
- `async ItemStatePredictedEvent(itemName)`
- `async ItemStateChangedEvent(itemName)`
- `async GroupItemStateChangedEvent(itemName, memberName)`

### AsyncThingEvents

The `AsyncThingEvents` class is the asynchronous counterpart to `ThingEvents`:

- `async ThingAddedEvent(thingUID)`
- `async ThingRemovedEvent(thingUID)`
- `async ThingUpdatedEvent(thingUID)`
- `async ThingStatusInfoEvent(thingUID)`
- `async ThingStatusInfoChangedEvent(thingUID)`

### AsyncInboxEvents

The `AsyncInboxEvents` class is the asynchronous counterpart to `InboxEvents`:

- `async InboxAddedEvent(thingUID)`
- `async InboxRemovedEvent(thingUID)`
- `async InboxUpdatedEvent(thingUID)`

### AsyncLinkEvents

The `AsyncLinkEvents` class is the asynchronous counterpart to `LinkEvents`:

- `async ItemChannelLinkAddedEvent(itemName, channelUID)`
- `async ItemChannelLinkRemovedEvent(itemName, channelUID)`

### AsyncChannelEvents

The `AsyncChannelEvents` class is the asynchronous counterpart to `ChannelEvents`:

- `async ChannelDescriptionChangedEvent(channelUID)`
- `async ChannelTriggeredEvent(channelUID)`

---

### Iconsets

The `Iconsets` class provides methods to interact with openHAB's iconsets.

#### Methods

##### `getIconsets(language: str = None) -> list`

Retrieves all available iconsets.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of available iconsets.

---

### AsyncIconsets

The `AsyncIconsets` class is the asynchronous counterpart to `Iconsets`:

- `async getIconsets(language)`

---

### Inbox

The `Inbox` class provides methods to interact with the openHAB inbox, which contains discovery results.

#### Initialization

```python
from openhab import OpenHABClient, Inbox

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
inbox = Inbox(client)
```

#### Methods

##### `getDiscoveredThings(includeIgnored: bool = True) -> list`

Retrieves all discovered things from the inbox.

**Parameters:**
- `includeIgnored` (bool, optional): Whether to include ignored results (default `True`).

**Returns:** A list of discovered things.

##### `removeDiscoveryResult(thingUID: str) -> dict`

Removes a discovery result from the inbox.

**Parameters:**
- `thingUID` (str): The UID of the thing to remove.

**Returns:** The response from the server.

##### `approveDiscoveryResult(thingUID: str, thingLabel: str, newThingID: str = None, language: str = None) -> dict`

Approves a discovery result and creates the corresponding thing.

**Parameters:**
- `thingUID` (str): The UID of the thing to approve.
- `thingLabel` (str): The label for the new thing.
- `newThingID` (str, optional): An optional new thing ID.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `ignoreDiscoveryResult(thingUID: str) -> dict`

Flags a discovery result as ignored.

**Parameters:**
- `thingUID` (str): The UID of the thing to ignore.

**Returns:** The response from the server.

##### `unignoreDiscoveryResult(thingUID: str) -> dict`

Removes the ignore flag from a discovery result.

**Parameters:**
- `thingUID` (str): The UID of the thing to unignore.

**Returns:** The response from the server.

---

### AsyncInbox

The `AsyncInbox` class is the asynchronous counterpart to `Inbox`:

- `async getDiscoveredThings(includeIgnored)`
- `async removeDiscoveryResult(thingUID)`
- `async approveDiscoveryResult(thingUID, thingLabel, newThingID, language)`
- `async ignoreDiscoveryResult(thingUID)`
- `async unignoreDiscoveryResult(thingUID)`

---

### Items

The `Items` class provides methods to interact with openHAB items via the REST API.

#### Initialization

```python
from openhab import OpenHABClient, Items

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
itemsAPI = Items(client)
```

#### Methods

##### `getItems(type: str = None, tags: str = None, metadata: str = ".*", recursive: bool = False, fields: str = None, staticDataOnly: bool = False, language: str = None)`

Gets all available items.

**Parameters:**
- `type` (str, optional): Item type filter.
- `tags` (str, optional): Item tag filter.
- `metadata` (str, optional): Metadata selector (default `".*"`).
- `recursive` (bool, optional): Fetch group members recursively (default `False`).
- `fields` (str, optional): Limit to specific fields (comma-separated).
- `staticDataOnly` (bool, optional): Only return cached data (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** A list containing all item data.

##### `addOrUpdateItems(items: list)`

Adds a list of items to the registry or updates existing items.

**Parameters:**
- `items` (list): A list of item data dictionaries.

**Returns:** Confirmation that the items were successfully added or updated.

##### `getItem(itemName: str, metadata: str = ".*", recursive: bool = True, language: str = None)`

Gets a single item.

**Parameters:**
- `itemName` (str): The name of the item.
- `metadata` (str, optional): Metadata selector (default `".*"`).
- `recursive` (bool, optional): Fetch group members recursively (default `True`).
- `language` (str, optional): Language for the response.

**Returns:** A dictionary containing the requested item data.

##### `addOrUpdateItem(itemName: str, itemData: dict, language: str = None)`

Adds a new item to the registry or updates the existing item.

**Parameters:**
- `itemName` (str): The name of the item.
- `itemData` (dict): The data of the item.
- `language` (str, optional): Language for the response.

**Returns:** Confirmation that the item was successfully added or updated.

##### `sendCommand(itemName: str, command: str, source: str = None)`

Sends a command to an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `command` (str): The command to send (e.g., `ON`, `OFF`).
- `source` (str, optional): Source of the command, shown in the event (openHAB 4.1+).

**Returns:** Confirmation that the command was successfully sent.

##### `postUpdate(itemName: str, state: str, source: str = None)`

Updates the state of an item. This is an alias for `updateItemState`.

**Parameters:**
- `itemName` (str): The name of the item.
- `state` (str): The state to be set.

##### `deleteItem(itemName: str)`

Removes an item from the registry.

**Parameters:**
- `itemName` (str): The name of the item.

**Returns:** Confirmation that the item was successfully deleted.

##### `addGroupMember(itemName: str, memberItemName: str)`

Adds a new member to a group item.

**Parameters:**
- `itemName` (str): The name of the group item.
- `memberItemName` (str): The name of the member item to add.

**Returns:** Confirmation that the group member was successfully added.

##### `removeGroupMember(itemName: str, memberItemName: str)`

Removes an existing member from a group item.

**Parameters:**
- `itemName` (str): The name of the group item.
- `memberItemName` (str): The name of the member item to remove.

**Returns:** Confirmation that the group member was successfully removed.

##### `addMetadata(itemName: str, namespace: str, metadata: dict)`

Adds metadata to an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `namespace` (str): The namespace of the metadata.
- `metadata` (dict): A dictionary containing the metadata.

**Returns:** Confirmation that the metadata was successfully added.

##### `removeMetadata(itemName: str, namespace: str)`

Removes metadata from an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `namespace` (str): The namespace of the metadata to remove.

**Returns:** Confirmation that the metadata was successfully removed.

##### `getMetadataNamespaces(itemName: str, language: str = None)`

Gets the namespaces of an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `language` (str, optional): Language for the response.

**Returns:** A list of namespaces associated with the item.

##### `getSemanticItem(itemName: str, semanticClass: str, language: str = None)`

Gets the item that defines the requested semantics of an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `semanticClass` (str): The requested semantic class.
- `language` (str, optional): Language for the response.

**Returns:** A dictionary containing the semantic item data.

##### `getItemState(itemName: str)`

Gets the state of an item.

**Parameters:**
- `itemName` (str): The name of the item.

**Returns:** The current state of the item as a string.

##### `updateItemState(itemName: str, state: str, language: str = None)`

Updates the state of an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `state` (str): The new state of the item.
- `language` (str, optional): Language for the response.

**Returns:** Confirmation that the state was successfully updated.

##### `addTag(itemName: str, tag: str)`

Adds a tag to an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `tag` (str): The tag to add.

**Returns:** Confirmation that the tag was successfully added.

##### `removeTag(itemName: str, tag: str)`

Removes a tag from an item.

**Parameters:**
- `itemName` (str): The name of the item.
- `tag` (str): The tag to remove.

**Returns:** Confirmation that the tag was successfully removed.

##### `purgeOrphanedMetadata()`

Removes unused/orphaned metadata from all items.

**Returns:** Confirmation that orphaned metadata was successfully purged.

---

### AsyncItems

The `AsyncItems` class is the asynchronous counterpart to `Items`. It provides the same methods as coroutines:

- `async getItems(type, tags, metadata, recursive, fields, staticDataOnly, language)`
- `async addOrUpdateItems(items)`
- `async getItem(itemName, metadata, recursive, language)`
- `async addOrUpdateItem(itemName, itemData, language)`
- `async sendCommand(itemName, command, source)`
- `async postUpdate(itemName, state, source)`
- `async updateItemState(itemName, state, language, source)`
- `async deleteItem(itemName)`
- `async addGroupMember(itemName, memberItemName)`
- `async removeGroupMember(itemName, memberItemName)`
- `async addMetadata(itemName, namespace, metadata)`
- `async removeMetadata(itemName, namespace)`
- `async getMetadataNamespaces(itemName, language)`
- `async getSemanticItem(itemName, semanticClass, language)`
- `async getItemState(itemName)`
- `async updateItemState(itemName, state, language)`
- `async addTag(itemName, tag)`
- `async removeTag(itemName, tag)`
- `async purgeOrphanedMetadata()`

---

### Links

The `Links` class provides methods to interact with openHAB item-channel links.

#### Initialization

```python
from openhab import OpenHABClient, Links

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
links = Links(client)
```

#### Methods

##### `getLinks(channelUID: str = None, itemName: str = None) -> list`

Gets all available links, optionally filtered by channel UID or item name.

**Parameters:**
- `channelUID` (str, optional): Filter by channel UID.
- `itemName` (str, optional): Filter by item name.

**Returns:** A list of links.

##### `getLink(itemName: str, channelUID: str) -> dict`

Retrieves an individual link between an item and a channel.

**Parameters:**
- `itemName` (str): The name of the item.
- `channelUID` (str): The UID of the channel.

**Returns:** The link details.

##### `linkItemToChannel(itemName: str, channelUID: str, configuration: dict) -> dict`

Links an item to a channel.

**Parameters:**
- `itemName` (str): The name of the item.
- `channelUID` (str): The UID of the channel.
- `configuration` (dict): The configuration for the link.

**Returns:** The API response when the link is successfully created.

##### `unlinkItemFromChannel(itemName: str, channelUID: str) -> dict`

Unlinks an item from a channel.

**Parameters:**
- `itemName` (str): The name of the item.
- `channelUID` (str): The UID of the channel.

**Returns:** The API response when the link is successfully removed.

##### `deleteAllLinks(object: str) -> dict`

Deletes all links that refer to an item or thing.

**Parameters:**
- `object` (str): The name of the item or the UID of the thing.

**Returns:** The API response when all links are successfully deleted.

##### `getOrphanLinks() -> list`

Gets orphan links between items and broken/non-existent thing channels.

**Returns:** A list of orphan links.

##### `purgeUnusedLinks() -> dict`

Removes all unused/orphaned links.

**Returns:** The API response when the links are successfully removed.

---

### AsyncLinks

The `AsyncLinks` class is the asynchronous counterpart to `Links`:

- `async getLinks(channelUID, itemName)`
- `async getLink(itemName, channelUID)`
- `async linkItemToChannel(itemName, channelUID, configuration)`
- `async unlinkItemFromChannel(itemName, channelUID)`
- `async deleteAllLinks(object)`
- `async getOrphanLinks()`
- `async purgeUnusedLinks()`

---

### Logging

The `Logging` class provides methods to interact with the openHAB logging system.

#### Initialization

```python
from openhab import OpenHABClient, Logging

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
logging_api = Logging(client)
```

#### Methods

##### `getLoggers() -> dict`

Gets all current loggers and their levels.

**Returns:** A dictionary containing all loggers.

##### `getLogger(loggerName: str) -> dict`

Gets a specific logger by name.

**Parameters:**
- `loggerName` (str): The name of the logger.

**Returns:** A dictionary containing the logger details.

##### `modifyOrAddLogger(loggerName: str, level: str) -> dict`

Modifies an existing logger or adds a new one.

**Parameters:**
- `loggerName` (str): The name of the logger.
- `level` (str): The log level (e.g., `DEBUG`, `INFO`, `WARN`, `ERROR`).

**Returns:** The response from the server.

##### `removeLogger(loggerName: str) -> dict`

Removes a logger by name.

**Parameters:**
- `loggerName` (str): The name of the logger to remove.

**Returns:** The response from the server.

---

### AsyncLogging

The `AsyncLogging` class is the asynchronous counterpart to `Logging`:

- `async getLoggers()`
- `async getLogger(loggerName)`
- `async modifyOrAddLogger(loggerName, level)`
- `async removeLogger(loggerName)`

---

### ModuleTypes

The `ModuleTypes` class provides methods to retrieve openHAB rule module types.

#### Methods

##### `getModuleTypes(tags=None, typeFilter=None, language: str = None)`

Gets all available module types.

**Parameters:**
- `tags` (optional): Filter by tags.
- `typeFilter` (optional): Filter by type (e.g., `trigger`, `condition`, `action`).
- `language` (str, optional): Language for the response.

**Returns:** A list of module types.

##### `getModuleType(moduleTypeUID, language: str = None)`

Gets a specific module type by its UID.

**Parameters:**
- `moduleTypeUID`: The UID of the module type.
- `language` (str, optional): Language for the response.

**Returns:** The module type details.

---

### AsyncModuleTypes

The `AsyncModuleTypes` class is the asynchronous counterpart to `ModuleTypes`:

- `async getModuleTypes(tags, typeFilter, language)`
- `async getModuleType(moduleTypeUID, language)`

---

### Persistence

The `Persistence` class provides methods to interact with openHAB's persistence services.

#### Initialization

```python
from openhab import OpenHABClient, Persistence

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
persistence = Persistence(client)
```

#### Methods

##### `getServices(language: str = None) -> dict`

Gets a list of persistence services.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of persistence services with IDs, labels, and types.

##### `getServiceConfiguration(serviceID: str) -> dict`

Gets the configuration of a specific persistence service.

**Parameters:**
- `serviceID` (str): The ID of the persistence service.

**Returns:** The configuration of the service.

##### `setServiceConfiguration(serviceID: str, config: dict) -> dict`

Sets the configuration of a persistence service.

**Parameters:**
- `serviceID` (str): The ID of the persistence service.
- `config` (dict): The configuration data.

**Returns:** The response from the API after modification.

##### `deleteServiceConfiguration(serviceID: str) -> dict`

Deletes the configuration of a persistence service.

**Parameters:**
- `serviceID` (str): The ID of the persistence service.

**Returns:** The response from the API after deleting the configuration.

##### `getItemsFromService(serviceID: str = None, itemName: str = None) -> list`

Gets a list of items available via a specific persistence service. Not every
service provides this information (rrd4j does not, inmemory and JDBC do).

**Parameters:**
- `serviceID` (str, optional): The ID of the persistence service.
- `itemName` (str, optional): Only return information for this item.

**Returns:** A list of items with their last and earliest timestamps.

##### `getItemPersistenceData(itemName: str, serviceID: str = None, startTime: str = None, endTime: str = None, page: int = None, pageLength: int = None, boundary: bool = False, itemState: bool = False, displayState: bool = None, language: str = None) -> dict`

Gets item persistence data from a persistence service.

**Parameters:**
- `itemName` (str): The name of the item.
- `serviceID` (str, optional): The ID of the persistence service (default service if omitted).
- `startTime` (str, optional): Start time in ISO 8601, e.g. `2026-10-30T00:00:00.000Z` (default: one day before `endTime`).
- `endTime` (str, optional): End time in ISO 8601 (default: now).
- `page` (int, optional): Page number, **starting at 0**. Only used together with `pageLength`.
- `pageLength` (int, optional): Data points per page. Without it, all data points of the time range are returned.
- `boundary` (bool, optional): Also return the values just outside the time range (default `False`).
- `itemState` (bool, optional): Append the current item state (default `False`).
- `displayState` (bool, optional): Add a formatted display state to every data point (openHAB 5.0+).
- `language` (str, optional): `Accept-Language` header.

**Returns:** The retrieved data points of the item.

##### `storeItemData(itemName: str, time: str, state: str, serviceID: str = None) -> dict`

Stores item persistence data into a persistence service.

**Parameters:**
- `itemName` (str): The name of the item.
- `time` (str): The timestamp for the data point.
- `state` (str): The state value to store.
- `serviceID` (str, optional): The ID of the persistence service.

**Returns:** The response from the API after storing the data.

##### `deleteItemData(itemName: str, startTime: str, endTime: str, serviceID: str) -> dict`

Deletes item persistence data from a persistence service within a given time range.

**Parameters:**
- `itemName` (str): The name of the item.
- `startTime` (str): The start time of the data to delete.
- `endTime` (str): The end time of the data to delete.
- `serviceID` (str): The ID of the persistence service.

**Returns:** The response from the API after deleting the data.

---

### AsyncPersistence

The `AsyncPersistence` class is the asynchronous counterpart to `Persistence`:

- `async getServices(language)`
- `async getServiceConfiguration(serviceID)`
- `async setServiceConfiguration(serviceID, config)`
- `async deleteServiceConfiguration(serviceID)`
- `async getItemsFromService(serviceID, itemName)`
- `async getItemPersistenceData(itemName, serviceID, startTime, endTime, page, pageLength, boundary, itemState, displayState, language)`
- `async storeItemData(itemName, time, state, serviceID)`
- `async deleteItemData(itemName, startTime, endTime, serviceID)`

---

### ProfileTypes

The `ProfileTypes` class provides methods to retrieve openHAB profile types.

#### Methods

##### `getProfileTypes(channelTypeUID=None, itemType=None, language: str = None)`

Gets all available profile types.

**Parameters:**
- `channelTypeUID` (optional): Filter by channel type UID.
- `itemType` (optional): Filter by item type.
- `language` (str, optional): Language for the response.

**Returns:** A list of profile types.

---

### AsyncProfileTypes

The `AsyncProfileTypes` class is the asynchronous counterpart to `ProfileTypes`:

- `async getProfileTypes(channelTypeUID, itemType, language)`

---

### Rules

The `Rules` class provides methods to interact with openHAB's rule engine.

#### Initialization

```python
from openhab import OpenHABClient, Rules

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
rules = Rules(client)
```

#### Methods

##### `getRules(prefix=None, tags=None, summary=False, staticDataOnly=False)`

Gets all available rules.

**Parameters:**
- `prefix` (optional): Filter by rule UID prefix.
- `tags` (optional): Filter by tags.
- `summary` (bool, optional): Return summary only (default `False`).
- `staticDataOnly` (bool, optional): Return only cached data (default `False`).

**Returns:** A list of rules.

##### `createRule(ruleData: dict)`

Creates a new rule.

**Parameters:**
- `ruleData` (dict): The rule data.

**Returns:** The response from the server.

##### `getRule(ruleUID: str)`

Gets a specific rule by its UID.

**Parameters:**
- `ruleUID` (str): The UID of the rule.

**Returns:** The rule details.

##### `updateRule(ruleUID: str, ruleData: dict)`

Updates an existing rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule to update.
- `ruleData` (dict): The new rule data.

**Returns:** The response from the server.

##### `deleteRule(ruleUID: str)`

Deletes a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule to delete.

**Returns:** The response from the server.

##### `getModule(ruleUID: str, moduleCategory: str, moduleID: str)`

Gets a specific module of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `moduleCategory` (str): The category of the module (e.g., `triggers`, `conditions`, `actions`).
- `moduleID` (str): The ID of the module.

**Returns:** The module details.

##### `getModuleConfig(ruleUID: str, moduleCategory: str, moduleID: str)`

Gets the configuration of a specific module.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `moduleCategory` (str): The module category.
- `moduleID` (str): The module ID.

**Returns:** The module configuration.

##### `getModuleConfigParam(ruleUID: str, moduleCategory: str, moduleID: str, param: str)`

Gets a specific configuration parameter of a module.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `moduleCategory` (str): The module category.
- `moduleID` (str): The module ID.
- `param` (str): The name of the parameter.

**Returns:** The parameter value.

##### `setModuleConfigParam(ruleUID: str, moduleCategory: str, moduleID: str, param: str, value: str)`

Sets a specific configuration parameter of a module.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `moduleCategory` (str): The module category.
- `moduleID` (str): The module ID.
- `param` (str): The name of the parameter.
- `value` (str): The value to set.

**Returns:** The response from the server.

##### `getActions(ruleUID: str)`

Gets the actions of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.

**Returns:** A list of action modules.

##### `getConditions(ruleUID: str)`

Gets the conditions of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.

**Returns:** A list of condition modules.

##### `getTriggers(ruleUID: str)`

Gets the triggers of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.

**Returns:** A list of trigger modules.

##### `getConfiguration(ruleUID: str)`

Gets the configuration of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.

**Returns:** The rule configuration.

##### `updateConfiguration(ruleUID: str, configData: dict)`

Updates the configuration of a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `configData` (dict): The new configuration data.

**Returns:** The response from the server.

##### `setRuleState(ruleUID: str, enable: bool)`

Enables or disables a rule.

**Parameters:**
- `ruleUID` (str): The UID of the rule.
- `enable` (bool): `True` to enable, `False` to disable.

**Returns:** The response from the server.

##### `enable(ruleUID: str)`

Enables a rule. Convenience wrapper for `setRuleState(ruleUID, True)`.

##### `disable(ruleUID: str)`

Disables a rule. Convenience wrapper for `setRuleState(ruleUID, False)`.

##### `runNow(ruleUID: str, contextData: dict = None)`

Executes a rule immediately.

**Parameters:**
- `ruleUID` (str): The UID of the rule to run.
- `contextData` (dict, optional): Optional context data for the rule execution.

**Returns:** The response from the server.

##### `simulateSchedule(fromTime: str, untilTime: str)`

Simulates the rule schedule between two timestamps.

**Parameters:**
- `fromTime` (str): The start timestamp.
- `untilTime` (str): The end timestamp.

**Returns:** The simulated schedule.

---

### AsyncRules

The `AsyncRules` class is the asynchronous counterpart to `Rules`:

- `async getRules(prefix, tags, summary, staticDataOnly)`
- `async createRule(ruleData)`
- `async getRule(ruleUID)`
- `async updateRule(ruleUID, ruleData)`
- `async deleteRule(ruleUID)`
- `async runNow(ruleUID, contextData)`
- `async enable(ruleUID)`
- `async disable(ruleUID)`
- `async setRuleState(ruleUID, enable)`
- `async getModule(ruleUID, moduleCategory, moduleID)`
- `async getModuleConfig(ruleUID, moduleCategory, moduleID)`
- `async getModuleConfigParam(ruleUID, moduleCategory, moduleID, param)`
- `async setModuleConfigParam(ruleUID, moduleCategory, moduleID, param, value)`
- `async getActions(ruleUID)`
- `async getConditions(ruleUID)`
- `async getConfiguration(ruleUID)`
- `async updateConfiguration(ruleUID, configData)`
- `async getTriggers(ruleUID)`
- `async simulateSchedule(fromTime, untilTime)`

---

### Services

The `Services` class provides methods to interact with openHAB's configurable services.

#### Initialization

```python
from openhab import OpenHABClient, Services

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
services = Services(client)
```

#### Methods

##### `getServices(language=None)`

Gets all configurable services.

**Parameters:**
- `language` (optional): Language for the response.

**Returns:** A list of services.

##### `getService(serviceID: str, language=None)`

Gets a specific service by ID.

**Parameters:**
- `serviceID` (str): The ID of the service.
- `language` (optional): Language for the response.

**Returns:** The service details.

##### `getServiceConfig(serviceID: str)`

Gets the configuration of a service.

**Parameters:**
- `serviceID` (str): The ID of the service.

**Returns:** The service configuration.

##### `updateServiceConfig(serviceID: str, configData: dict, language: str = None)`

Updates the configuration of a service.

**Parameters:**
- `serviceID` (str): The ID of the service.
- `configData` (dict): The new configuration data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `deleteServiceConfig(serviceID: str)`

Deletes the configuration of a service.

**Parameters:**
- `serviceID` (str): The ID of the service.

**Returns:** The response from the server.

##### `getServiceContexts(serviceID: str, language=None)`

Gets all contexts of a multi-context service.

**Parameters:**
- `serviceID` (str): The ID of the service.
- `language` (optional): Language for the response.

**Returns:** A list of service contexts.

---

### AsyncServices

The `AsyncServices` class is the asynchronous counterpart to `Services`:

- `async getServices(language)`
- `async getService(serviceID, language)`
- `async getServiceConfig(serviceID)`
- `async updateServiceConfig(serviceID, configData, language)`
- `async deleteServiceConfig(serviceID)`
- `async getServiceContexts(serviceID, language)`

---

### Sitemaps

The `Sitemaps` class provides methods to interact with openHAB sitemaps.

#### Initialization

```python
from openhab import OpenHABClient, Sitemaps

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
sitemaps = Sitemaps(client)
```

#### Methods

##### `getSitemaps()`

Gets all available sitemaps.

**Returns:** A list of sitemaps.

##### `getSitemap(sitemapName: str, type: str = None, jsonCallback: str = None, includeHidden: bool = False, language: str = None)`

Gets a specific sitemap.

**Parameters:**
- `sitemapName` (str): The name of the sitemap.
- `type` (str, optional): The type of subscription.
- `jsonCallback` (str, optional): JSONP callback name.
- `includeHidden` (bool, optional): Include hidden widgets (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** The sitemap data.

##### `getSitemapPage(sitemapName: str, pageID: str, subscriptionID: str = None, includeHidden: bool = False, language: str = None)`

Gets a specific page of a sitemap.

**Parameters:**
- `sitemapName` (str): The name of the sitemap.
- `pageID` (str): The ID of the page.
- `subscriptionID` (str, optional): The subscription ID for real-time updates.
- `includeHidden` (bool, optional): Include hidden widgets (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** The sitemap page data.

##### `getFullSitemap(sitemapName: str, subscriptionID: str = None, includeHidden: bool = False, language: str = None)`

Gets the full sitemap including all pages.

**Parameters:**
- `sitemapName` (str): The name of the sitemap.
- `subscriptionID` (str, optional): The subscription ID for real-time updates.
- `includeHidden` (bool, optional): Include hidden widgets (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** The full sitemap data.

##### `getSitemapEvents(subscriptionID: str, sitemapName: str = None, pageID: str = None)`

Gets sitemap events for a given subscription, optionally filtered by sitemap and page.

**Parameters:**
- `subscriptionID` (str): The ID of the subscription.
- `sitemapName` (str, optional): The name of the sitemap to filter by.
- `pageID` (str, optional): The ID of the page to filter by.

**Returns:** An SSE event stream for sitemap updates.

##### `getFullSitemapEvents(subscriptionID: str, sitemapName: str = None)`

Gets full sitemap events for a given subscription.

**Parameters:**
- `subscriptionID` (str): The ID of the subscription.
- `sitemapName` (str, optional): The name of the sitemap to filter by.

**Returns:** An SSE event stream for full sitemap updates.

##### `subscribeToSitemapEvents()`

Creates a new subscription for sitemap events.

**Returns:** `{"message": "Subscription created.", "location": "<url>", "subscriptionID": "<id>"}`.

---

### AsyncSitemaps

The `AsyncSitemaps` class is the asynchronous counterpart to `Sitemaps`:

- `async getSitemaps()`
- `async getSitemap(sitemapName, type, jsonCallback, includeHidden, language)`
- `async getSitemapPage(sitemapName, pageID, subscriptionID, includeHidden, language)`
- `async getFullSitemap(sitemapName, subscriptionID, includeHidden, language)`
- `async getSitemapEvents(subscriptionID, sitemapName, pageID)`
- `async getFullSitemapEvents(subscriptionID, sitemapName)`
- `async subscribeToSitemapEvents()`

---

### Systeminfo

The `Systeminfo` class provides methods to retrieve openHAB system information.

#### Methods

##### `getSystemInfo()`

Gets general system information.

**Returns:** A dictionary containing system information.

##### `getUoMInfo()`

Gets units of measurement information.

**Returns:** A dictionary containing UoM information.

---

### AsyncSysteminfo

The `AsyncSysteminfo` class is the asynchronous counterpart to `Systeminfo`:

- `async getSystemInfo()`
- `async getUoMInfo()`

---

### Tags

The `Tags` class provides methods to interact with openHAB semantic tags.

#### Initialization

```python
from openhab import OpenHABClient, Tags

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
tags = Tags(client)
```

#### Methods

##### `getTags(language: str = None)`

Gets all available semantic tags.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of semantic tags.

##### `createTag(tagData, language: str = None)`

Creates a new semantic tag.

**Parameters:**
- `tagData`: The tag data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `getTag(tagID: str, language: str = None)`

Gets a specific semantic tag by ID.

**Parameters:**
- `tagID` (str): The ID of the tag.
- `language` (str, optional): Language for the response.

**Returns:** The tag details.

##### `updateTag(tagID: str, tagData, language: str = None)`

Updates an existing semantic tag.

**Parameters:**
- `tagID` (str): The ID of the tag to update.
- `tagData`: The new tag data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `deleteTag(tagID: str, language: str = None)`

Deletes a semantic tag.

**Parameters:**
- `tagID` (str): The ID of the tag to delete.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

---

### AsyncTags

The `AsyncTags` class is the asynchronous counterpart to `Tags`:

- `async getTags(language)`
- `async createTag(tagData, language)`
- `async getTag(tagID, language)`
- `async updateTag(tagID, tagData, language)`
- `async deleteTag(tagID, language)`

---

### Templates

The `Templates` class provides methods to retrieve openHAB rule templates.

#### Methods

##### `getTemplates(language: str = None) -> list`

Gets all available templates.

**Parameters:**
- `language` (str, optional): Language for the response.

**Returns:** A list of templates.

##### `getTemplate(templateUID: str, language: str = None) -> dict`

Gets a specific template by its UID.

**Parameters:**
- `templateUID` (str): The UID of the template.
- `language` (str, optional): Language for the response.

**Returns:** The template details.

---

### AsyncTemplates

The `AsyncTemplates` class is the asynchronous counterpart to `Templates`:

- `async getTemplates(language)`
- `async getTemplate(templateUID, language)`

---

### ThingTypes

The `ThingTypes` class provides methods to retrieve openHAB thing types.

#### Methods

##### `getThingTypes(bindingID: str = None, language: str = None) -> list`

Gets all available thing types.

**Parameters:**
- `bindingID` (str, optional): Filter by binding ID.
- `language` (str, optional): Language for the response.

**Returns:** A list of thing types.

##### `getThingType(thingTypeUID: str, language: str = None) -> dict`

Gets a specific thing type by its UID.

**Parameters:**
- `thingTypeUID` (str): The UID of the thing type.
- `language` (str, optional): Language for the response.

**Returns:** The thing type details.

---

### AsyncThingTypes

The `AsyncThingTypes` class is the asynchronous counterpart to `ThingTypes`:

- `async getThingTypes(bindingID, language)`
- `async getThingType(thingTypeUID, language)`

---

### Things

The `Things` class provides methods to interact with openHAB things.

#### Initialization

```python
from openhab import OpenHABClient, Things

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
things = Things(client)
```

#### Methods

##### `getThings(summary: bool = False, staticDataOnly: bool = False, language: str = None)`

Gets all available things.

**Parameters:**
- `summary` (bool, optional): Return summary only (default `False`).
- `staticDataOnly` (bool, optional): Return only cached data (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** A list of things.

##### `createThing(thingData: dict, language: str = None)`

Creates a new thing.

**Parameters:**
- `thingData` (dict): The thing data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `getThing(thingUID: str, language: str = None)`

Gets a specific thing by its UID.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `language` (str, optional): Language for the response.

**Returns:** The thing details.

##### `updateThing(thingUID: str, thingData: dict, language: str = None)`

Updates an existing thing.

**Parameters:**
- `thingUID` (str): The UID of the thing to update.
- `thingData` (dict): The new thing data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `deleteThing(thingUID: str, force: bool = False, language: str = None)`

Deletes a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing to delete.
- `force` (bool, optional): Force deletion even if the thing is linked (default `False`).
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `updateThingConfiguration(thingUID: str, configurationData: dict, language: str = None)`

Updates the configuration of a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `configurationData` (dict): The new configuration data.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `getThingConfigStatus(thingUID: str, language: str = None)`

Gets the configuration status of a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `language` (str, optional): Language for the response.

**Returns:** The configuration status.

##### `setThingStatus(thingUID: str, enabled: bool, language: str = None)`

Enables or disables a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `enabled` (bool): `True` to enable, `False` to disable.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `enableThing(thingUID: str)`

Enables a thing. Convenience wrapper for `setThingStatus(thingUID, True)`.

##### `disableThing(thingUID: str)`

Disables a thing. Convenience wrapper for `setThingStatus(thingUID, False)`.

##### `updateThingFirmware(thingUID: str, firmwareVersion: str, language: str = None)`

Updates the firmware of a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `firmwareVersion` (str): The firmware version to install.
- `language` (str, optional): Language for the response.

**Returns:** The response from the server.

##### `getThingFirmwareStatus(thingUID: str, language: str = None)`

Gets the firmware status of a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `language` (str, optional): Language for the response.

**Returns:** The firmware status.

##### `getThingFirmwares(thingUID: str, language: str = None)`

Gets all available firmware versions for a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `language` (str, optional): Language for the response.

**Returns:** A list of available firmware versions.

##### `getThingStatus(thingUID: str, language: str = None)`

Gets the status of a thing.

**Parameters:**
- `thingUID` (str): The UID of the thing.
- `language` (str, optional): Language for the response.

**Returns:** The thing status.

---

### AsyncThings

The `AsyncThings` class is the asynchronous counterpart to `Things`:

- `async getThings(summary, staticDataOnly, language)`
- `async createThing(thingData, language)`
- `async getThing(thingUID, language)`
- `async updateThing(thingUID, thingData, language)`
- `async deleteThing(thingUID, force, language)`
- `async updateThingConfiguration(thingUID, configurationData, language)`
- `async getThingConfigStatus(thingUID, language)`
- `async setThingStatus(thingUID, enabled, language)`
- `async enableThing(thingUID)`
- `async disableThing(thingUID)`
- `async updateThingFirmware(thingUID, firmwareVersion, language)`
- `async getThingFirmwareStatus(thingUID, language)`
- `async getThingFirmwares(thingUID, language)`
- `async getThingStatus(thingUID, language)`

---

### Transformations

The `Transformations` class provides methods to interact with transformations in the openHAB system.

#### Methods

##### `getTransformations()`

Retrieves a list of all transformations.

**Returns:** A list of transformations (JSON).

##### `getTransformation(transformationUID: str)`

Gets a single transformation by its UID.

**Parameters:**
- `transformationUID` (str): The UID of the transformation to retrieve.

**Returns:** The transformation (JSON).

##### `updateTransformation(transformationUID: str, transformationData)`

Updates a single transformation.

**Parameters:**
- `transformationUID` (str): The UID of the transformation to update.
- `transformationData`: The new data for the transformation.

**Returns:** The response to the transformation update request.

##### `deleteTransformation(transformationUID: str)`

Deletes a single transformation by its UID.

**Parameters:**
- `transformationUID` (str): The UID of the transformation to delete.

**Returns:** The response to the transformation delete request.

##### `getTransformationServices()`

Gets all transformation services available.

**Returns:** A list of transformation services (JSON).

---

### AsyncTransformations

The `AsyncTransformations` class is the asynchronous counterpart to `Transformations`:

- `async getTransformations()`
- `async getTransformation(transformationUID)`
- `async updateTransformation(transformationUID, transformationData)`
- `async deleteTransformation(transformationUID)`
- `async getTransformationServices()`

---

### UI

The `UI` class provides methods to interact with UI components and tiles in the openHAB system.

#### Methods

##### `getUIComponents(namespace: str, summary: bool = False)`

Retrieves all registered UI components within the specified namespace.

**Parameters:**
- `namespace` (str): The namespace for which UI components should be retrieved.
- `summary` (bool, optional): If `True`, only summary fields will be returned (default `False`).

**Returns:** A list of UI components (JSON).

##### `addUIComponent(namespace: str, componentData)`

Adds a UI component to the specified namespace.

**Parameters:**
- `namespace` (str): The namespace where the UI component should be added.
- `componentData`: The data of the UI component to be added (JSON).

**Returns:** The response to the request (JSON).

##### `getUIComponent(namespace: str, componentUID: str)`

Retrieves a specific UI component in the specified namespace.

**Parameters:**
- `namespace` (str): The namespace where the UI component is located.
- `componentUID` (str): The UID of the UI component to retrieve.

**Returns:** The UI component (JSON).

##### `updateUIComponent(namespace: str, componentUID: str, componentData)`

Updates a specific UI component in the specified namespace.

**Parameters:**
- `namespace` (str): The namespace where the UI component should be updated.
- `componentUID` (str): The UID of the UI component to update.
- `componentData`: The new data for the UI component (JSON).

**Returns:** The response to the request (JSON).

##### `deleteUIComponent(namespace: str, componentUID: str)`

Removes a specific UI component from the specified namespace.

**Parameters:**
- `namespace` (str): The namespace where the UI component should be removed.
- `componentUID` (str): The UID of the UI component to delete.

**Returns:** The response to the request (JSON).

##### `getUITiles()`

Retrieves all registered UI tiles.

**Returns:** A list of UI tiles (JSON).

---

### AsyncUI

The `AsyncUI` class is the asynchronous counterpart to `UI`:

- `async getUIComponents(namespace, summary)`
- `async addUIComponent(namespace, componentData)`
- `async getUIComponent(namespace, componentUID)`
- `async updateUIComponent(namespace, componentUID, componentData)`
- `async deleteUIComponent(namespace, componentUID)`
- `async getUITiles()`

---

### UUID

The `UUID` class provides a method to retrieve a unified unique identifier from the openHAB system.

#### Methods

##### `getUUID() -> str`

Retrieves the UUID of the openHAB instance.

**Returns:** A string containing the UUID.

---

### AsyncUUID

The `AsyncUUID` class is the asynchronous counterpart to `UUID`:

- `async getUUID()`

---

### Voice

The `Voice` class provides methods to interact with the voice processing system, including starting and stopping dialogs, interpreting text, and speaking text aloud.

#### Initialization

```python
from openhab import OpenHABClient, Voice

client = OpenHABClient("http://openhab-server:8080", username="user", password="pass")
voice = Voice(client)
```

#### Methods

##### `getDefaultVoice(language: str = None)`

Gets the default voice used by the system.

**Returns:** A dictionary with details of the default voice.

##### `getVoices(language: str = None)`

Gets the list of all voices.

**Returns:** A list of voices.

##### `getInterpreters(language: str = None)`

Gets the list of all interpreters.

**Parameters:**
- `language` (str, optional): The language for the request.

**Returns:** A list of interpreters.

##### `getInterpreter(interpreterID: str, language: str = None)`

Gets a single interpreter.

**Parameters:**
- `interpreterID` (str): The ID of the interpreter.
- `language` (str, optional): The language for the request.

**Returns:** The details of the interpreter.

##### `interpretText(text: str, language: str = None)`

Sends a text to the default human language interpreter.

**Parameters:**
- `text` (str): The text to be interpreted.
- `language` (str, optional): The language of the text.

**Returns:** The response from the server.

##### `interpretTextBatch(text: str, IDs: list, language: str = None)`

Sends a text to given human language interpreter(s).

**Parameters:**
- `text` (str): The text to be interpreted.
- `IDs` (list): A list of interpreter IDs.
- `language` (str, optional): The language of the text.

**Returns:** The response from the server.

##### `startDialog(sourceID: str, ksID: str = None, sttID: str = None, ttsID: str = None, voiceID: str = None, hliIDs: str = None, sinkID: str = None, keyword: str = None, listeningItem: str = None)`

Starts dialog processing for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.
- `ksID` (str, optional): The ID of the keyword spotter.
- `sttID` (str, optional): The ID of the speech-to-text system.
- `ttsID` (str, optional): The ID of the text-to-speech system.
- `voiceID` (str, optional): The ID of the voice.
- `hliIDs` (str, optional): A comma-separated list of interpreter IDs.
- `sinkID` (str, optional): The ID of the audio output.
- `keyword` (str, optional): The keyword used to start the dialog.
- `listeningItem` (str, optional): The name of the item to listen to.

**Returns:** The response from the server.

##### `stopDialog(sourceID: str)`

Stops dialog processing for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.

**Returns:** The response from the server.

##### `listenAndAnswer(sourceID: str, sttID: str, ttsID: str, voiceID: str, hliIDs: list = None, sinkID: str = None, listeningItem: str = None)`

Executes a simple dialog sequence without keyword spotting for a given audio source.

**Parameters:**
- `sourceID` (str): The ID of the audio source.
- `sttID` (str): The ID of the speech-to-text system.
- `ttsID` (str): The ID of the text-to-speech system.
- `voiceID` (str): The ID of the voice.
- `hliIDs` (list, optional): A list of interpreter IDs.
- `sinkID` (str, optional): The ID of the audio output.
- `listeningItem` (str, optional): The name of the item to listen to.

**Returns:** The response from the server.

##### `sayText(text: str, voiceID: str, sinkID: str, volume: str = '100')`

Speaks a given text with a given voice through the given audio sink.

**Parameters:**
- `text` (str): The text to be spoken.
- `voiceID` (str): The ID of the voice.
- `sinkID` (str): The ID of the audio output.
- `volume` (str, optional): The volume level (default: `100`).

**Returns:** The response from the server.

---

### AsyncVoice

The `AsyncVoice` class is the asynchronous counterpart to `Voice`. It provides the same methods as coroutines:

- `async getDefaultVoice(language)`
- `async getVoices(language)`
- `async getInterpreters(language)`
- `async getInterpreter(interpreterID, language)`
- `async interpretText(text, language)`
- `async interpretTextBatch(text, IDs, language)`
- `async startDialog(sourceID, ksID, sttID, ttsID, voiceID, hliIDs, sinkID, keyword, listeningItem)`
- `async stopDialog(sourceID)`
- `async listenAndAnswer(sourceID, sttID, ttsID, voiceID, hliIDs, sinkID, listeningItem)`
- `async sayText(text, voiceID, sinkID, volume)`

---

## Contributing

Contributions are welcome! Please create an issue or pull request to suggest changes.

We welcome contributions to improve **python-openhab-rest-client**!

### How to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

Please ensure your code adheres to PEP 8 guidelines and includes relevant documentation and tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Changelog

### 21.4.0

Bug fixes (all found against openHAB 5.2.3):

- **Async events:** `AsyncEvents`, `AsyncItemEvents`, … called the non-existent
  `AsyncOpenHABClient.executeSSE()`. The method now exists (public) and returns the open
  `aiohttp` response. SSE streams are no longer cut after the aiohttp default timeout of 5 minutes.
- **SSE and token authentication:** the synchronous SSE request did not use the client
  session, so the `Authorization: Bearer` header was missing (`401`). It now uses the
  session (token and Basic Authentication) and reports errors properly.
- **Responses with a `status` field:** the internal marker `{"status": <code>}` for empty
  responses collided with JSON that contains a `status` field. `Things.getThingStatus()`
  and `Rules.getRule()`/`getRules()` returned `"Unexpected response"` instead of the data.
  Empty responses are now represented by the dedicated type `StatusResponse`.
- **`ItemEvents.ItemEvent()`** subscribed to `openhab/items` (no events at all); now `openhab/items/*`.
- **Persistence:** the query parameter was sent as `serviceID` instead of `serviceId`, so
  openHAB silently used the default service. `getItemPersistenceData()` used `page=1`,
  which skipped the first page (pages start at 0) – paging is now off by default and all
  data points of the time range are returned. `getItemsFromService()` builds its query
  correctly and explains `405`.
- **`Items.addOrUpdateItem()`** sent `Accept: */` and always failed with `406`.
- **`Rules.createRule()`** crashed with `AttributeError` (`response.status_code`).
- **`Rules.runNow()`** sent its body without content type (`415` in the async variant).
- **`Links`:** `linkItemToChannel()` put the URL-encoded channel UID into the JSON body
  (`400 Content does not match the path`); `getLink()` reported a missing link as
  "Content does not match the path".
- **UIDs containing `#`** (action and channel UIDs such as `astro.getElevation#…`) were cut
  off as URL fragment, e.g. `Actions.executeAction()` always returned "Action not found".
- **`Inbox.approveDiscoveryResult()`:** `newThingID` → `newThingId`.
- **`Sitemaps`:** `subscriptionID`/`pageId` → `subscriptionid`/`pageid`;
  `subscribeToSitemapEvents()` now returns the subscription ID and URL.
- **`Voice`:** `sayText()` sent `voiceId`/`sinkId` instead of `voiceid`/`sinkid`;
  `interpretTextBatch()` used the wrong endpoint.
- **`Addons`:** `serviceId` for install/uninstall/config is sent as query parameter.
- **`Services.updateServiceConfig()`** reported `204` (no previous configuration) as error.
- The client no longer changes the session headers permanently with every request
  (a `Content-Type` of one request leaked into all following requests).

Improvements:

- The asynchronous classes are generated from the synchronous ones
  (`tools/generate_async.py`) and now return exactly the same values and messages –
  previously many async methods returned the raw `{"status": 200}`.
- Error messages contain openHAB's own explanation, e.g.
  `... (Persistence service not modifiable: rrd4j)`.
- Clearer messages for rejected commands/states (`Invalid command for this item.`).
- New optional parameters: `timeout` and `verify` for both clients;
  `source` for `sendCommand`/`postUpdate`/`updateItemState`; `parents` for `getItems`/`getItem`;
  `displayState`/`language` for `getItemPersistenceData`; `itemName` for `getItemsFromService`;
  `language` for `Voice.getVoices`/`getDefaultVoice`.
- `OpenHABClient` can be used as context manager (`with OpenHABClient(...) as client:`),
  `AsyncOpenHABClient` creates its session lazily and has `close()`.
- **Events arrived late:** SSE streams are now requested uncompressed (`Accept-Encoding: identity`);
  a gzip-compressed stream was flushed by openHAB only with the next message.
  New helpers `iterSSELines`, `iterSSEEvents`, `aiterSSELines`, `aiterSSEEvents` and `parseSSEData`
  deliver every event immediately – `requests`' `iter_lines()` keeps the last line of a chunk back.
- Text responses are decoded as UTF-8 (`getItemState` returned `21.5 Â°C` instead of `21.5 °C`).
- `StatusResponse` is exported. Automated tests (`tests_pytest/`), `pyproject.toml`.
