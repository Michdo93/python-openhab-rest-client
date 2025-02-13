import json
import sys
import os

# Add the project root path (one level up) to the Python search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openhab import OpenHABClient, Auth

def testGetApiTokens(authAPI: Auth, language: str = None):
    """Test retrieving all API tokens."""
    print("\n~~~~ Test #1: getApiTokens() ~~~~\n")
    
    try:
        tokens = authAPI.getApiTokens(language)
        print("API Tokens:", json.dumps(tokens, indent=4))
    except Exception as e:
        print(f"Error retrieving API tokens: {e}")

def testRevokeApiToken(authAPI: Auth, tokenName: str, language: str = None):
    """Test revoking an API token."""
    print("\n~~~~ Test #2: revokeApiToken() ~~~~\n")

    try:
        revokeResponse = authAPI.revokeApiToken(tokenName, language)
        print("Token revoked:", json.dumps(revokeResponse, indent=4))
    except Exception as e:
        print(f"Error revoking API token: {e}")

def testGetSessions(authAPI: Auth, language: str = None):
    """Test retrieving active sessions."""
    print("\n~~~~ Test #3: getSessions() ~~~~\n")

    try:
        sessions = authAPI.getSessions(language)
        print("Sessions:", json.dumps(sessions, indent=4))
    except Exception as e:
        print(f"Error retrieving sessions: {e}")

def testGetToken(authAPI: Auth, grantType: str, code: str = None, redirectUri: str = None, clientID: str = None, refreshToken: str = None, codeVerifier: str = None, language: str = None):
    """Test obtaining an access token using the authorization code flow."""
    print("\n~~~~ Test #4: getToken(grantType, code, redirectUri, clientID, refreshToken, codeVerifier) ~~~~\n")

    try:
        tokenResponse = authAPI.getToken(grantType=grantType, code=code, redirectUri=redirectUri, clientID=clientID, refreshToken=refreshToken, codeVerifier=codeVerifier, language=language)

        if "error" in tokenResponse:
            print(f"Error in token response: {tokenResponse['error']}")
        else:
            print("Token Response:", json.dumps(tokenResponse, indent=4))
        return tokenResponse  # Return response for further testing
    except Exception as e:
        print(f"Exception occurred while retrieving token: {e}")
        return None

def testLogout(authAPI: Auth, tokenResponse: dict, language: str = None):
    """Test logging out using a valid refresh token."""
    print("\n~~~~ Test #5: logout() ~~~~\n")

    if tokenResponse and "refresh_token" in tokenResponse:
        refreshToken = tokenResponse["refresh_token"]
        try:
            logoutResponse = authAPI.logout(refreshToken=refreshToken, language=language)
            print("Logout Response:", json.dumps(logoutResponse, indent=4))
        except Exception as e:
            print(f"Error during logout: {e}")
    else:
        print("No refresh token available. Logout not possible.")

if __name__ == "__main__":
    # Initialize OpenHAB client (replace with your OpenHAB URL and authentication details)
    client = OpenHABClient(url="http://127.0.0.1:8080", username="openhab", password="habopen")
    authAPI = Auth(client)

    tokenName = "openhab"

    grantType="authorization_code"  # Specify the grant type
    code="test-auth-code"           # Replace with a valid authorization code
    redirectUri="http://localhost"  # Replace with the actual redirect URI
    clientID="test-client-id"       # Replace with a valid client ID

    # Run all tests
    testGetApiTokens(authAPI)               # Test #1
    testRevokeApiToken(authAPI, tokenName)  # Test #2
    testGetSessions(authAPI)                # Test #3
    tokenResponse = testGetToken(
        authAPI,
        grantType=grantType,
        code=code,
        redirectUri=redirectUri,
        clientID=clientID
    )                                       # Test #4
    testLogout(authAPI, tokenResponse)      # Test #5
