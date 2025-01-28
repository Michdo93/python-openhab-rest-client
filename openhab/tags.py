from .client import OpenHABClient

class Tags:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Tags-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_tags(self, language=None):
        """
        Holt alle verfügbaren semantischen Tags.

        :param language: Optionaler Header für die Spracheinstellung.

        :return: Eine Liste der semantischen Tags (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.get("/tags", headers=headers)

    def create_tag(self, tag_data, language=None):
        """
        Erstellt ein neues semantisches Tag und fügt es dem Tag-Register hinzu.

        :param tag_data: Das Datenobjekt für das Tag, das erstellt werden soll.
        :param language: Optionaler Header für die Spracheinstellung.

        :return: Die Antwort auf die Tag-Erstellungsanforderung (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.post("/tags", json=tag_data, headers=headers)

    def get_tag(self, tag_id: str, language=None):
        """
        Holt ein semantisches Tag und seine Untertags anhand der Tag-ID.

        :param tag_id: Die ID des Tags, das abgerufen werden soll.
        :param language: Optionaler Header für die Spracheinstellung.

        :return: Das Tag-Objekt und seine Untertags (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.get(f"/tags/{tag_id}", headers=headers)

    def update_tag(self, tag_id: str, tag_data, language=None):
        """
        Aktualisiert ein semantisches Tag anhand der Tag-ID.

        :param tag_id: Die ID des Tags, das aktualisiert werden soll.
        :param tag_data: Die neuen Tag-Daten.
        :param language: Optionaler Header für die Spracheinstellung.

        :return: Die Antwort auf die Tag-Aktualisierungsanforderung (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.put(f"/tags/{tag_id}", json=tag_data, headers=headers)

    def delete_tag(self, tag_id: str, language=None):
        """
        Entfernt ein semantisches Tag und seine Untertags aus dem Tag-Register.

        :param tag_id: Die ID des Tags, das entfernt werden soll.
        :param language: Optionaler Header für die Spracheinstellung.

        :return: Die Antwort auf die Tag-Löschanforderung (JSON).
        """
        headers = {"Accept-Language": language} if language else {}
        return self.client.delete(f"/tags/{tag_id}", headers=headers)
