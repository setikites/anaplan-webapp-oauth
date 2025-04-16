
# Table of Contents

1.  [Install](#org48a8eaf)
2.  [Run](#org8c0c13c)
3.  [References](#orgd5d5a3d)
    1.  [Anaplan](#orgc2b7c0b)
    2.  [Python](#org962e12c)
4.  [Inspiration](#orgacb90bd)

Anaplan provides a robust API that can be used to interact with the
Anaplan platform.  This sample code shows how to authenticate using
OAuth2 and obtain an access token that will permit use of the Anaplan
API.

This sample code uses the python package requests-oauthlib


<a id="org48a8eaf"></a>

# Install

The steps below outline how to use the OAuth2 Authorization Code Grant
type flow to obtain an access token and fetch a protected resource. In
this example the provider is Anaplan and the protected resource is the
user’s profile.

create a virtual environment

    python -m venv venv

activate a virtual environment (non-Windows)

    . venv/bin/activate

activate a virtual environment (Windows)

    venv\Scripts\activate

add the required packages

-   **requests-oauthlib:** for managing OAuth2 authentication
-   **flask:** for simple web app
-   **pyopenssl:** for flask to use https

    pip install -r requirements.txt


<a id="org8c0c13c"></a>

# Run

Setup an OAuth Client in the Anaplan Administration Security
console, (type: Authorization code grant). When you have obtained a
client<sub>id</sub>, client<sub>secret</sub>, and registered a callback URL then you can
try out the command line interactive example below.  The script
expects to find client<sub>id</sub> in shell variable CLIENT and client<sub>secret</sub>
in shell variable SECRET.

    python anaplan.py

OAuth 2 providers may allow you to refresh access tokens using refresh
tokens. Commonly, only clients that authenticate may refresh tokens,
e.g. web applications but not javascript clients. The provider will
mention whether they allow token refresh in their API documentation
and if you see a “refresh<sub>token</sub>” in your token response you are good
to go.

This example shows how a simple web application (using the Flask web
framework) can refresh Anaplan OAuth 2 tokens. It should be trivial to
transfer to any other web framework and provider.

Flask runs the development web application at <https://127.0.0.1:5000>
After the web app sends you to Anaplan to login, it will deliver code
and state values to the redirect URL (<https://www.anaplan.com>).  You
will need to edit the callback URL to <https://127.0.0.1:5000/callback>
for the web application to proceed with authentication.  You can use a
bookmarklet to make this edit for you

    javascript:(function()
                {window.location=window.location.toString().replace(/^https:\/\/www\.anaplan\.com\//,'https://127.0.0.1:5000/callback');})()

    python main.py


<a id="orgd5d5a3d"></a>

# References

For additional documentation, see the following


<a id="orgc2b7c0b"></a>

## Anaplan

-   <https://help.anaplan.com/oauth-clients-f08ae7da-2224-46ff-a8c6-b7eb75d2b65d>
-   <https://community.anaplan.com/discussion/156943/anaplans-authorization-code-grant-api-flow-a-seamless-app-to-app-authentication-option>
-   <https://anaplanoauth2service.docs.apiary.io/>#
-   <https://anaplanauthentication.docs.apiary.io/>#
-   <https://anaplan.docs.apiary.io/#/introduction>


<a id="org962e12c"></a>

## Python

-   <https://requests-oauthlib.readthedocs.io/en/latest/index.html>
-   <https://oauthlib.readthedocs.io/en/latest/oauth2/oauth2.html>


<a id="orgacb90bd"></a>

# Inspiration

<https://github.com/qkeddy/anaplan-python-oauth-example>

