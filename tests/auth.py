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
authApi = Auth(client)

# 1. Alle API-Tokens abrufen
tokens = authApi.getApiTokens()
print("API Tokens:", tokens)

# 2. Ein API-Token widerrufen
#revokeResponse = authApi.revokeApiToken("openhab")
#print("Token widerrufen:", revokeResponse)

# 3. Sessions abfragen
#sessions = authApi.getSessions()
#print("Sessions:", json.dumps(sessions, indent=4))

# 4. Refresh-Token erstellen (simuliert durch einen spezifischen API-Endpunkt oder OAuth)
# Ersetzt die Parameter durch gültige Werte, falls erforderlich
tokenResponse = authApi.getToken(
    grantType="authorization_code",  # Für die Demo: Nutze einen gültigen grantType
    code="your-auth-code",
    redirectUri="http://127.0.0.1",
    clientID="your-client-id"
)
print("Token Response:", json.dumps(tokenResponse, indent=4))

# 5. Mit einem gültigen Refresh-Token abmelden
refreshToken = tokenResponse.get("refresh_token", "")
if refreshToken:
    logoutResponse = authApi.logout(refreshToken=refreshToken)
    print("Logout Response:", json.dumps(logoutResponse, indent=4))
else:
    print("Kein Refresh-Token vorhanden. Abmelden nicht möglich.")
