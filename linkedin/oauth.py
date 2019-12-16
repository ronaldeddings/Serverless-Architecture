from requests_oauthlib import OAuth2Session
import os
import json
import urllib.parse

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
BASE_URL = os.environ["BASE_URL"]

TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken' 

def oauth(event, context):
    queryStringParameters = event.get("queryStringParameters", {})

    if not queryStringParameters or not queryStringParameters.get("state") or not queryStringParameters.get("code"):
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": f'Missing URI Parameters. Navigate to the <a href="{BASE_URL}/login">Login Page</a> to restart.'
        }

    state = queryStringParameters.get("state")
    encodedParameters = urllib.parse.urlencode(queryStringParameters)
    requestUrl = f"{BASE_URL}?{encodedParameters}"
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=state)

    try:
        token = linkedin.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            include_client_id=True,
            authorization_response=requestUrl,
            verify=False
        )
    except:
         return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": f'The application failed to fetch an Oauth token. Navigate to <a href="{BASE_URL}/login">Login Page</a> to restart.'
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(token)
    }
    return response
