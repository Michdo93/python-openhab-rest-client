from .client import OpenHABClient
import json

class Items:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Items-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def create(self):
        pass
    
    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def get_all_items(
        self,
        language: str = None,
        type: str = None,
        tags: str = None,
        metadata: str = ".*",
        recursive: bool = False,
        fields: str = None,
        static_data_only: bool = False,
    ):
        """
        Ruft alle verfügbaren Items ab.

        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :param type: Optional; Item-Typ-Filter.
        :param tags: Optional; Item-Tag-Filter.
        :param metadata: Optional; Metadaten-Selektor (Standard: .*).
        :param recursive: Optional; Rekursives Abrufen von Gruppenmitgliedern (Standard: False).
        :param fields: Optional; Begrenzung auf bestimmte Felder (komma-separiert).
        :param static_data_only: Optional; Liefert nur Cache-Daten (Standard: False).
        :return: Die Antwort der API (JSON oder Text).
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "type": type,
            "tags": tags,
            "metadata": metadata,
            "recursive": str(recursive).lower(),
            "fields": fields,
            "staticDataOnly": str(static_data_only).lower(),
        }

        # Entferne None-Werte aus den Parametern
        params = {key: value for key, value in params.items() if value is not None}

        return self.client.get("/items", header=header, params=params)

    def add_or_update_items(self, items: list):
        """
        Fügt eine Liste von Items hinzu oder aktualisiert bestehende Items.

        :param items: Eine Liste von Item-Daten (Dictionary).
        :return: Die Antwort der API.
        """
        header = {"Content-Type": "application/json"}  # Korrekte Header

        # JSON-kodierte Daten
        items = json.dumps(items)

        return self.client.put("/items", data=items, header=header)  # json-Parameter verwenden

    def get_item(self, item_name: str, language: str = None, metadata: str = ".*", recursive: bool = True):
        """
        Ruft ein einzelnes Item ab.

        :param item_name: Der Name des Items.
        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :param metadata: Optional; Metadaten-Selektor (Standard: .*).
        :param recursive: Optional; Rekursives Abrufen von Gruppenmitgliedern (Standard: True).
        :return: Die Antwort der API (JSON oder Text).
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        params = {
            "metadata": metadata,
            "recursive": str(recursive).lower(),
        }

        return self.client.get(f"/items/{item_name}", header=header, params=params)

    def add_or_update_item(self, item_name: str, item_data: dict, language: str = None):
        """
        Fügt ein Item hinzu oder aktualisiert es.

        :param item_name: Der Name des Items.
        :param item_data: Die Daten des Items (Dictionary).
        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :return: Die Antwort der API.
        """
        header = {
            "Content-Type": "application/json"
        }
        if language:
            header["Accept-Language"] = language

        # JSON-kodierte Daten
        json_data = json.dumps(item_data)
        
        return self.client.put(f"/items/{item_name}", header=header, data=json_data)

    def send_command(self, item_name: str, command: str):
        """
        Sendet einen Befehl an ein Item.

        :param item_name: Der Name des Items.
        :param command: Der Befehl, der gesendet werden soll (z.B. ON, OFF).
        :return: Die Antwort der API.
        """
        header = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}

        return self.client.post(f"/items/{item_name}", header=header, data=command)

    def post_update(self, item_name: str, state: str):
        """
        Aktualisiert den Zustand eines Items ohne direkten Einfluss auf den tatsächlichen Zustand.
        Dies wird häufig verwendet, um den Zustand eines Items zu signalisieren, ohne ihn direkt zu setzen.

        :param item_name: Der Name des Items.
        :param state: Der Zustand, der für das Item signalisiert werden soll.
        :return: Die Antwort der API.
        """
        return self.update_item_state(item_name, state)

    def delete_item(self, item_name: str):
        """
        Entfernt ein Item aus dem Registry.

        :param item_name: Der Name des Items.
        :return: Die Antwort der API.
        """
        return self.client.delete(f"/items/{item_name}")

    def add_group_member(self, item_name: str, member_item_name: str):
        """
        Fügt ein neues Mitglied zu einem Gruppen-Item hinzu.

        :param item_name: Der Name des Gruppen-Items.
        :param member_item_name: Der Name des Mitglied-Items.
        :return: Die Antwort der API.
        """
        return self.client.put(f"/items/{item_name}/members/{member_item_name}")

    def remove_group_member(self, item_name: str, member_item_name: str):
        """
        Entfernt ein Mitglied aus einem Gruppen-Item.

        :param item_name: Der Name des Gruppen-Items.
        :param member_item_name: Der Name des Mitglied-Items.
        :return: Die Antwort der API.
        """
        return self.client.delete(f"/items/{item_name}/members/{member_item_name}")

    def add_metadata(self, item_name: str, namespace: str, metadata: dict):
        """
        Fügt einem Item Metadaten hinzu.

        :param item_name: Der Name des Items.
        :param namespace: Der Namespace der Metadaten.
        :param metadata: Ein Dictionary mit den Metadaten.
        :return: Die Antwort der API.
        """
        # Setze den Header für JSON-Daten
        header = {"Content-Type": "application/json"}

        # Konvertiere das Dictionary in JSON
        json_data = json.dumps(metadata)

        # Sende die Anfrage mit JSON-Daten
        return self.client.put(f"/items/{item_name}/metadata/{namespace}", header=header, data=json_data)

    def remove_metadata(self, item_name: str, namespace: str):
        """
        Entfernt Metadaten aus einem Item.

        :param item_name: Der Name des Items.
        :param namespace: Der Namespace der Metadaten.
        :return: Die Antwort der API.
        """
        return self.client.delete(f"/items/{item_name}/metadata/{namespace}")

    def get_metadata_namespaces(self, item_name: str, language: str = None):
        """
        Ruft die verfügbaren Metadaten-Namespaces eines Items ab.

        :param item_name: Der Name des Items.
        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :return: Die Antwort der API.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/items/{item_name}/metadata/namespaces", header=header)

    def get_semantic_item(self, item_name: str, semantic_class: str, language: str = None):
        """
        Ruft das Item ab, das die angeforderte Semantik definiert.

        :param item_name: Der Name des Items.
        :param semantic_class: Die angeforderte Semantik-Klasse.
        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :return: Die Antwort der API.
        """
        header = {}
        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/items/{item_name}/semantic/{semantic_class}", header=header)

    def get_item_state(self, item_name: str):
        """
        Ruft den Zustand eines Items ab.

        :param item_name: Der Name des Items.
        :return: Die Antwort der API (Zustand des Items).
        """
        return self.client.get(f"/items/{item_name}/state")

    def update_item_state(self, item_name: str, state: str, language: str = None):
        """
        Aktualisiert den Zustand eines Items.

        :param item_name: Der Name des Items.
        :param state: Der neue Zustand des Items.
        :param language: Optional; Sprachfilter für Header "Accept-Language".
        :return: Die Antwort der API.
        """
        header = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}
        if language:
            header["Accept-Language"] = language

        return self.client.put(f"/items/{item_name}/state", header=header, data=state)
            
    def add_tag(self, item_name: str, tag: str):
        """
        Fügt einem Item ein Tag hinzu.

        :param item_name: Der Name des Items.
        :param tag: Der hinzuzufügende Tag.
        :return: Die Antwort der API.
        """

        #header = {"Content-Type": "application/json"}
        # Hier kein expliziter Content-Type nötig, Authorization wird von OpenHABClient verwaltet.
        return self.client.put(f"/items/{item_name}/tags/{tag}")

    def remove_tag(self, item_name: str, tag: str):
        """
        Entfernt einen Tag von einem Item.

        :param item_name: Der Name des Items.
        :param tag: Der zu entfernende Tag.
        :return: Die Antwort der API.
        """
        return self.client.delete(f"/items/{item_name}/tags/{tag}")

    def purge_orphaned_metadata(self):
        """
        Entfernt ungenutzte oder verwaiste Metadaten.

        :return: Die Antwort der API.
        """
        return self.client.post("/items/metadata/purge")
