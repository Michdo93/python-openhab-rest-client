from .client import OpenHABClient

class ModuleTypes:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die ModuleTypes-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_module_types(self, tags=None, type_filter=None, language: str = None):
        """
        Ruft alle verfügbaren Modultypen ab.

        :param tags: Optionaler Filter für Tags.
        :param type_filter: Optionaler Filter für den Typ (action, condition, trigger).
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Modultypen.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        params = {}
        if tags:
            params["tags"] = tags
        if type_filter:
            params["type"] = type_filter

        return self.client.get("/module-types", params=params, header=header)

    def get_module_type(self, module_type_uid, language: str = None):
        """
        Ruft einen spezifischen Modultyp anhand der UID ab.

        :param module_type_uid: Die UID des Modultyps.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Ein Dictionary mit den Modultypinformationen.
        """
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get(f"/module-types/{module_type_uid}", header=header)
