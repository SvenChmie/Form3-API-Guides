#### Authentication Snippet ####
# Obtains a bearer token.

# Note: This snippet differs from the snippet in the API docs. 
# It defines the Content-Type in the header, which is necessary for the call to work.

import requests

# Please make sure to fill in your personal client ID and your client secret before running this snippet!
client_id = 'YOUR CLIENT ID GOES HERE'
client_secret = 'YOUR CLIENT SECRET GOES HERE'

payload = "grant_type=client_credentials"
base_url = 'https://api.tabla.env.form3.tech/v1'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
auth_request = requests.auth.HTTPBasicAuth(client_id, client_secret)

request = requests.request('post', base_url + '/oauth2/token', data=payload, auth=auth_request, headers=headers)
print request.content