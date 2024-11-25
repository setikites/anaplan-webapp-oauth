"""Based on Google OAuth 2 Tutorial from
https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
"""
import os

# Credentials you get from registering a new application
client_id = os.environ["CLIENT"]
client_secret = os.environ["SECRET"]
redirect_uri = "https://www.anaplan.com"

import json


def pretty_json(j_res):
    return json.dumps(j_res, indent=4)


# OAuth endpoints given in the Anaplan API documentation
authorization_base_url = "https://us1a.app.anaplan.com/auth/prelogin"
token_url = "https://us1a.app.anaplan.com/oauth/token"
scope = ["openid", "email", "offline_access"]

# Customize token type for Anaplan - did not work
# from odd_web_application import OddWebApplicationClient
# anaplan_client = OddWebApplicationClient (client_id, token_type='AnaplanAuthToken')

from requests_oauthlib import OAuth2Session

anaplan = OAuth2Session(
    client_id, scope=scope, redirect_uri=redirect_uri
)  # failed with client=anaplan_client

# Redirect user to Anaplan for authorization
authorization_url, state = anaplan.authorization_url(
    authorization_base_url,
    # offline for refresh token
    # force to always make user click authorize
    access_type="offline",
    prompt="select_account",
)
print("Please go here and authorize:", authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input("Paste the full redirect URL here: ")

# Fetch the access token
token = anaplan.fetch_token(
    token_url, client_secret=client_secret, authorization_response=redirect_response
)
print("\n=== TOKEN ===")
print(pretty_json(token))

# Fetch a protected resource, i.e. user profile
r = anaplan.get("https://api.anaplan.com/2/0/users/me")
print("\n=== ME ===")
print(pretty_json(r.json()))


import requests

headers = {"Authorization": f'AnaplanAuthToken {token["access_token"]}'}

# Validation fails because Anaplan does not expect a Bearer token
r = requests.get("https://auth.anaplan.com/token/validate", headers=headers)
print("\n=== VALIDATION ===")
print(pretty_json(r.json()))
