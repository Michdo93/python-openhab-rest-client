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

Supports both Server-Sent Events (SSE) and regular REST requests. SSE is used for the events of openHAB.

## Requirements

- Python 3.x
- `requests`
- `json`

## Installation

Install via pip:

```sh
pip install python-openhab-rest-client
```

## Usage

Basically, you always need the `OpenHABClient`. Regardless of whether you carry out a normal `REST request` or one via `SSE`. This looks as follows:

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

allItems = itemsAPI.getAllItems()
print("All Items:", allItems)
```

#### Server-sent Events (SSE) requests

All normal REST requests are static. This means that they do not react to status changes. You would therefore have to send several REST requests in succession (polling). Or you can use the various evetnts from openHAB. This can be done using server-sent events (SSE) without polling. The server sends a message to the client exactly when it can make something available. With polling, on the other hand, you would have to constantly send requests to the server, which would significantly increase the network and server load.

There are various [events](https://www.openhab.org/docs/developer/utils/events.html) in openHAB. For `ItemEvents`, `ThingEvents`, `InboxEvents`, `LinkEvents` and `ChannelEvents` there are own classes. However, there is also the `Events` class. More information can be found in the documentation.

An example looks like this:

```python
from openhab import OpenHABClient, ItemEvents

client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
itemEvents = ItemEvents(client)

response =  itemEvents.ItemStateChangedEvent()

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

## Full list of Methods

### Actions

### Addons

### Audio

### Auth

### ChannelTypes

### ConfigDescriptions

### Discovery

### Events

#### ItemEvents

#### ThingEvents

#### InboxEvents

#### LinkEvents

#### ChannelEvents

### Iconsets

### Inbox

### Items

### Links

### Logging

### ModuleTypes

### Persistence

### ProfileTypes

### Rules

### Services

### Sitemaps

### Systeminfo

### Tags

### Templates

### ThingTypes

### Things

### Transformations

### UI

### UUID

### Voice

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
