#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### Authentication Snippet ####
# Obtains a bearer token.

import requests

### Replace these variables with your own data! ###
client_id = 'YOUR CLIENT ID HERE'
client_secret = 'YOUR CLIENT SECRET HERE'

auth_payload = "grant_type=client_credentials"
auth_url = 'https://api.test.form3.tech/v1/oauth2/token'
auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
auth_request = requests.auth.HTTPBasicAuth(client_id, client_secret)

auth = requests.request('post', auth_url, data=auth_payload, auth=auth_request, headers=auth_headers)
print(auth.content)

print("Bearer token: %s" % auth.json().get('access_token'))


