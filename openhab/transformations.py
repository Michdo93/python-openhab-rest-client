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


"""
from client import OpenHABClient
from transformations import Transformations

# OpenHABClient instanziieren
client = OpenHABClient(base_url="http://your-openhab-instance:8080")
transformations = Transformations(client)

# Alle Transformationen abrufen
transformations_list = transformations.get_transformations()
print(transformations_list)

# Eine spezifische Transformation abrufen
uid = "your-transformation-uid"
transformation = transformations.get_transformation(uid)
print(transformation)

# Eine Transformation aktualisieren
updated_data = {
    "uid": "your-transformation-uid",
    "label": "Updated Label",
    "type": "new-type",
    "configuration": {
        "additionalProp1": "value1",
        "additionalProp2": "value2"
    },
    "editable": True
}
updated_transformation = transformations.update_transformation(uid, updated_data)
print(updated_transformation)

# Eine Transformation löschen
deleted_transformation = transformations.delete_transformation(uid)
print(deleted_transformation)

# Alle Transformation-Dienste abrufen
services = transformations.get_transformation_services()
print(services)


"""