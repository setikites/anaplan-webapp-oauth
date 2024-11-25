"""Based on Refreshing tokens in OAuth 2 from
https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example_with_refresh.html
"""

import os
from pprint import pformat
from time import time

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import requests
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)

# This information is obtained upon creating an Anaplan OAuth client
# Authorization Code Grant on Anaplan Adminstration Security console.
client_id = os.environ["CLIENT"]
client_secret = os.environ["SECRET"]
redirect_uri = "https://www.anaplan.com"

# Uncomment for detailed oauthlib logs
# import logging
# import sys
# log = logging.getLogger('oauthlib')
# log.addHandler(logging.StreamHandler(sys.stdout))
# log.setLevel(logging.DEBUG)

# OAuth endpoints given in the Anaplan OAuth2 Service API documentation
# at https://anaplanoauth2service.docs.apiary.io/#
authorization_base_url = "https://us1a.app.anaplan.com/auth/prelogin"
token_url = "https://us1a.app.anaplan.com/oauth/token"
refresh_url = token_url
scope = ["openid", "email", "offline_access"]


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Anaplan)
    using an URL with a few key OAuth parameters.
    """
    anaplan = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = anaplan.authorization_url(
        authorization_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline",
        prompt="select_account",
    )

    # State is used to prevent CSRF, keep this for later.
    session["oauth_state"] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@app.route("/callback", methods=["GET"])
def callback():
    """Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    anaplan = OAuth2Session(
        client_id, redirect_uri=redirect_uri, state=session["oauth_state"]
    )
    token = anaplan.fetch_token(
        token_url, client_secret=client_secret, authorization_response=request.url
    )

    # We use the session as a simple DB for this example.
    session["oauth_token"] = token

    return redirect(url_for(".menu"))


@app.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/profile"> Get account profile</a></li>
        <li><a href="/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/validate"> Validate the token</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(
        session["oauth_token"]["access_token"], indent=4
    )


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token."""
    anaplan = OAuth2Session(client_id, token=session["oauth_token"])
    return jsonify(anaplan.get("https://api.anaplan.com/2/0/users/me").json())


@app.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token."""
    token = session["oauth_token"]

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Anaplan API.
    token["expires_at"] = time() - 10

    extra = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    def token_updater(token):
        session["oauth_token"] = token

    anaplan = OAuth2Session(
        client_id,
        token=token,
        auto_refresh_kwargs=extra,
        auto_refresh_url=refresh_url,
        token_updater=token_updater,
    )

    # Trigger the automatic refresh
    jsonify(anaplan.get("https://api.anaplan.com/2/0/users/me").json())
    return jsonify(session["oauth_token"])


@app.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token."""
    token = session["oauth_token"]

    extra = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    anaplan = OAuth2Session(client_id, token=token)
    session["oauth_token"] = anaplan.refresh_token(refresh_url, **extra)
    return jsonify(session["oauth_token"])


@app.route("/validate", methods=["GET"])
def validate():
    """Validate a token with the OAuth provider Anaplan."""
    token = session["oauth_token"]

    validate_url = "https://auth.anaplan.com/token/validate"

    headers = {"Authorization": f'AnaplanAuthToken {token["access_token"]}'}

    # No OAuth2Session is needed, just a plain GET request
    return jsonify(requests.get(validate_url, headers=headers).json())


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, ssl_context="adhoc")
