from .client import OpenHABClient

class Templates:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Templates-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_all_templates(self, language: str = None) -> list:
        """
        Ruft alle verfügbaren Templates ab.

        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Eine Liste von Templates.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = "/templates"
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)

    def get_template_by_uid(self, template_uid: str, language: str = None) -> dict:
        """
        Ruft ein Template anhand seiner UID ab.

        :param template_uid: Die UID des Templates.
        :param language: (Optional) Spracheinstellung für den Accept-Language-Header.
        :return: Ein Dictionary mit den Details des Templates.
        :raises: Eine Exception, falls der Request fehlschlägt.
        """
        endpoint = f"/templates/{template_uid}"
        header = {"Content-Type": "application/json"}

        if language:
            header["Accept-Language"] = language

        return self.client.get(endpoint, header=header)
