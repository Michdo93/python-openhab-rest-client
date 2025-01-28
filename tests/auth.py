import json
import sys
import os

# Füge den Projektwurzelpfad (eine Ebene höher) zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Auth

# openhab
# habopen
# oh.openhab.U0doM1Lz4kJ6tPlVGjH17jjm4ZcTHIHi7sMwESzrIybKbCGySmBMtysPnObQLuLf7PgqnI7jWQ5LosySY8Q

# Client initialisieren
client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
auth_api = Auth(client)

# 1. Alle API-Tokens abrufen
#tokens = auth_api.get_api_tokens()
#print("API Tokens:", tokens)

# 2. Ein API-Token widerrufen
#revoke_response = auth_api.revoke_api_token("openhab")
#print("Token widerrufen:", revoke_response)

# 3. Sessions abfragen
sessions = auth_api.get_sessions()
print("Sessions:", json.dumps(sessions, indent=4))

# 4. Refresh-Token erstellen (simuliert durch einen spezifischen API-Endpunkt oder OAuth)
# Ersetzt die Parameter durch gültige Werte, falls erforderlich
token_response = auth_api.get_token(
    grant_type="authorization_code",  # Für die Demo: Nutze einen gültigen grant_type
    code="your-auth-code",
    redirect_uri="http://127.0.0.1",
    client_id="your-client-id"
)
print("Token Response:", json.dumps(token_response, indent=4))

# 5. Mit einem gültigen Refresh-Token abmelden
refresh_token = token_response.get("refresh_token", "")
if refresh_token:
    logout_response = auth_api.logout(refresh_token=refresh_token)
    print("Logout Response:", json.dumps(logout_response, indent=4))
else:
    print("Kein Refresh-Token vorhanden. Abmelden nicht möglich.")
