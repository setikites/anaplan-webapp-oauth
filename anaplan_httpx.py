"""Based on Google OAuth 2 Tutorial from
https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
"""

# Credentials you get from creating a new Authorizaiton Code Grant type OAuth 2.0 client in Anaplan
# https://help.anaplan.com/create-an-oauth-20-client-0984a799-a667-4e70-8759-a134be32f48c
import os
import json
import httpx
from _auth import AnaplanCodeGrantAuth


client_id = os.environ["CLIENT"]
client_secret = os.environ["SECRET"]
redirect_uri = "https://www.anaplan.com"


def pretty_json(j_res):
    return json.dumps(j_res, indent=4)


# OAuth endpoints given in the Anaplan API documentation
# https://anaplanoauth2service.docs.apiary.io/#
authorization_base_url = "https://us1a.app.anaplan.com/auth/prelogin"
token_url = "https://us1a.app.anaplan.com/oauth/token"
scope = ["openid", "email", "offline_access"]  # error when including "profile"

auth = AnaplanCodeGrantAuth(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Anaplan for authorization
authorization_url, state = auth.authorization_url(authorization_base_url)
print("Please go here and authorize:", authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input("Paste the full redirect URL here: ")

# Fetch the access token
token = auth.fetch_token(
    token_url, client_secret=client_secret, authorization_response=redirect_response
)
print("\n=== TOKEN ===")
print(pretty_json(token))

anaplan = httpx.Client(auth=auth)

# Fetch a protected resource, i.e. user profile
r = anaplan.get("https://api.anaplan.com/2/0/users/me")
print("\n=== ME ===")
print(pretty_json(r.json()))

# must use AnaplanAuthToken for validation.  Bearer will not validate
headers = {"Authorization": f"AnaplanAuthToken {token['access_token']}"}

# No OAuth2Session is needed, just a plain GET request
r = httpx.get("https://auth.anaplan.com/token/validate", headers=headers)
print("\n=== VALIDATION ===")
print(pretty_json(r.json()))
