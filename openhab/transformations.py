from .client import OpenHABClient

class Transformations:
    def __init__(self, client: OpenHABClient):
        """
        Initialisiert die Transformations-Klasse mit einem OpenHABClient-Objekt.

        :param client: Eine Instanz von OpenHABClient, die für die REST-API-Kommunikation verwendet wird.
        """
        self.client = client

    def get_transformations(self):
        """
        Holt eine Liste aller verfügbaren Transformationen.

        :return: Eine Liste von Transformationen (JSON).
        """
        return self.client.get("/transformations")

    def get_transformation(self, uid: str):
        """
        Holt eine einzelne Transformation anhand der UID.

        :param uid: Die UID der Transformation, die abgerufen werden soll.
        :return: Die Transformation (JSON).
        """
        return self.client.get(f"/transformations/{uid}")

    def update_transformation(self, uid: str, transformation_data):
        """
        Aktualisiert eine Transformation anhand der UID.

        :param uid: Die UID der Transformation, die aktualisiert werden soll.
        :param transformation_data: Die neuen Daten der Transformation.
        :return: Die Antwort auf die Transformations-Aktualisierungsanforderung (JSON).
        """
        return self.client.put(f"/transformations/{uid}", json=transformation_data)

    def delete_transformation(self, uid: str):
        """
        Löscht eine Transformation anhand der UID.

        :param uid: Die UID der Transformation, die gelöscht werden soll.
        :return: Die Antwort auf die Transformations-Löschanforderung (JSON).
        """
        return self.client.delete(f"/transformations/{uid}")

    def get_transformation_services(self):
        """
        Holt eine Liste aller verfügbaren Transformation-Dienste.

        :return: Eine Liste von Transformation-Diensten (JSON).
        """
        return self.client.get("/transformations/services")