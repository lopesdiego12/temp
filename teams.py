import json
import requests
import yaml
from requests_oauthlib import OAuth2Session

def load_oauth_settings():
    with open('oauth_settings.yml', 'r') as stream:
        settings = yaml.load(stream, yaml.SafeLoader)
    return settings

def get_sign_in_url():
    settings = load_oauth_settings()
    aad_auth = OAuth2Session(settings['app_id'], scope=settings['scopes'], redirect_uri=settings['redirect'])
    sign_in_url, state = aad_auth.authorization_url(settings['authority'] + settings['authorize_endpoint'], prompt='login')
    return sign_in_url, state

def get_access_token(code):
    settings = load_oauth_settings()
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        'client_id': settings['app_id'],
        'scope': settings['scopes'],
        'code': code,
        'redirect_uri': settings['redirect'],
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)
    response_data = json.loads(response.text)
    return response_data.get('access_token')

def get_sharepoint_sites():
    access_token = get_access_token('your_authorization_code_here')
    response = requests.get('https://graph.microsoft.com/v1.0/sites?search=your_site_name', headers={'Authorization': f'Bearer {access_token}'})
    return response.text

def get_sharepoint_data():
    access_token = get_access_token('your_authorization_code_here')
    response = requests.get('https://graph.microsoft.com/v1.0/sites/your_site_id/drive/root:/General/Recordings:/children', headers={'Authorization': f'Bearer {access_token}'})
    return response.json()

# Example usage:
# sign_in_url, state = get_sign_in_url()
# print(f"Sign-in URL: {sign_in_url}")
# sharepoint_sites = get_sharepoint_sites()
# print(f"SharePoint sites: {sharepoint_sites}")
# sharepoint_data = get_sharepoint_data()
# print(f"SharePoint data: {sharepoint_data}")
