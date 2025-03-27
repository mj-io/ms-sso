import os
import json
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
import requests
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView

__version__ = "0.5.0"


@settings.AUTH.login_required
def index(request, *, context):
    return render(request, 'index.html', dict(
        user=context['user'],
        edit_profile_url=settings.AUTH.get_edit_profile_url(),
        api_endpoint=os.getenv("ENDPOINT"),
        title=f"Microsoft Entra ID Django Web App Sample v{__version__}",
    ))

@settings.AUTH.login_required(scopes=os.getenv("SCOPE", "").split())
def call_api(request, *, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render(request, 'display.html', {
        "title": "Result of API call",
        "content": json.dumps(api_result, indent=4),
    })

@api_view(['GET'])
def microsoft_id_api(request):
    data = {
        "associatedApplications": [
            {"applicationId": "8f406c2f-1e7d-453d-ad20-e8eacb5f0abe"}
        ]
    }
    return JsonResponse(data)

class MsOauth2Adapter(OAuth2Adapter):
    """
    Microsoft OAuth2.0 adapter
    """
    provider_id = 'microsoft'
    access_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    authorize_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    profile_url = 'https://graph.microsoft.com/v1.0/me'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, headers={
            'Authorization': 'Bearer ' + token.token
        })
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)

class MsOauth2LoginView(OAuth2LoginView):
    adapter_class = MsOauth2Adapter
    callback_url = reverse_lazy('socialaccount_callback')

