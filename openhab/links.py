from .client import OpenHABClient
import json
from urllib.parse import quote

class Links:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Links-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_links(self, channel_uid: str = None, item_name: str = None) -> list:
        """
        Ruft alle verfügbaren Links ab, mit optionalen Filtern nach Channel UID oder Item Name.

        :param channel_uid: Optional, Filtert nach der Channel UID.
        :param item_name: Optional, Filtert nach dem Item Name.
        :return: Eine Liste von Links, die Details wie ItemName, ChannelUID und Konfiguration enthalten.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/links"
        header = {"Content-Type": "application/json"}
        params = {}
        if channel_uid:
            params["channelUID"] = channel_uid
        if item_name:
            params["itemName"] = item_name
        
        return self.client.get(endpoint, params=params, header=header)

    def get_individual_link(self, item_name: str, channel_uid: str) -> dict:
        """
        Ruft einen einzelnen Link anhand des Item Names und der Channel UID ab.

        :param item_name: Der Name des Items.
        :param channel_uid: Die UID des Channels.
        :return: Der Link mit den Details des Items, Channel UID und Konfiguration.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        item_name = quote(item_name, safe="")
        channel_uid = quote(channel_uid, safe="")
        endpoint = f"/links/{item_name}/{channel_uid}"
        header = {"Accept": "application/json"}
        
        return self.client.get(endpoint, header=header)

    def link_item_to_channel(self, item_name: str, channel_uid: str, configuration: dict) -> dict:
        """
        Verknüpft ein Item mit einem Channel.

        :param item_name: Der Name des Items.
        :param channel_uid: Die UID des Channels.
        :param configuration: Die Konfiguration für den Link.
        :return: Die Antwort der API, wenn der Link erfolgreich erstellt wurde.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        item_name = quote(item_name, safe="")
        channel_uid = quote(channel_uid, safe="")
        endpoint = f"/links/{item_name}/{channel_uid}"
        header = {"Content-Type": "application/json"}
        data = json.dumps({
            "itemName": item_name,
            "channelUID": channel_uid,
            "configuration": configuration
        })

        print(data)
        
        return self.client.put(endpoint, data=data, header=header)

    def unlink_item_from_channel(self, item_name: str, channel_uid: str) -> dict:
        """
        Entfernt die Verknüpfung eines Items mit einem Channel.

        :param item_name: Der Name des Items.
        :param channel_uid: Die UID des Channels.
        :return: Die Antwort der API, wenn der Link erfolgreich entfernt wurde.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        item_name = quote(item_name, safe="")
        channel_uid = quote(channel_uid, safe="")
        endpoint = f"/links/{item_name}/{channel_uid}"
        header = {"Content-Type": "application/json"}
        
        return self.client.delete(endpoint, header=header)

    def delete_all_links(self, object: str) -> dict:
        """
        Löscht alle Links, die sich auf ein Item oder Thing beziehen.

        :param object: Der Name des Items oder die UID des Things.
        :return: Die Antwort der API, wenn alle Links erfolgreich gelöscht wurden.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = f"/links/{object}"
        
        return self.client.delete(endpoint)

    def get_orphan_links(self) -> list:
        """
        Ruft alle Orphan-Links ab, d.h. Links zu nicht existierenden oder defekten Channels.

        :return: Eine Liste von Orphan-Links.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/links/orphans"
        header = {"Accept": "application/json"}
        
        return self.client.get(endpoint, header=header)

    def purge_unused_links(self) -> dict:
        """
        Entfernt alle ungenutzten oder orphaned Links.

        :return: Die Antwort der API, wenn die Links erfolgreich entfernt wurden.
        :raises Exception: Wenn die Anfrage fehlschlägt.
        """
        endpoint = "/links/purge"
        
        return self.client.post(endpoint)
