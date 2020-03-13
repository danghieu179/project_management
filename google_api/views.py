from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import requests
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = os.path.dirname(
    os.path.abspath(__file__)) + "/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


class AuthorizeView(View):
    def get(self, request):
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES)
        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = request.build_absolute_uri(
            reverse('oauth2callback'))
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            prompt='select_account',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        # Store the state so the callback can verify the auth server response.
        request.session['state'] = state
        return redirect(authorization_url)


class Oauth2CallbackView(View):
    def get(self, request):
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = request.session['state']
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = request.build_absolute_uri(
            reverse('oauth2callback'))

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)
        redirect_url = request.session['redirect_url']
        return redirect(reverse(redirect_url))


class RevokeView(View):
    def get(self, request):
        if 'credentials' not in request.session:
            return redirect(reverse('index'))
        credentials = Credentials(
            **request.session['credentials'])
        revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                               params={'token': credentials.token},
                               headers={'content-type': 'application/x-www-form-urlencoded'}, verify=False)
        status_code = getattr(revoke, 'status_code')
        request.session.pop('credentials', None)
        if status_code == 200:
            return redirect(reverse('index'))
        return redirect(reverse('index'))
