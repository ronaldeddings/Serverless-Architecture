from requests_oauthlib import OAuth2Session
import os

SCOPE = os.environ["SCOPE"].split(",")
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
TOKEN_URL = os.environ["TOKEN_URL"]
AUTHORIZE_URL = os.environ["AUTHORIZE_URL"]


def login(event, context):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    login_url, _ = oauth.authorization_url(AUTHORIZE_URL)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": f'<a href="{login_url}">To Login Click Here</a>'
    }
