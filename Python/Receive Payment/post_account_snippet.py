#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Creating Account Snippet ###
# Creates an account.

import uuid, requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
bank_id = 'YOUR UK SORTCODE HERE'
bic = 'YOUR BIC HERE'
account_number = 'A VALID ACCOUNT NUMBER HERE'
customer_id =  'A VALID CUSTOMER ID HERE'

# Generate IDs
acc_id = uuid.uuid4()
print("Account ID: %s" % acc_id)

acc_url = "https://api.test.form3.tech/v1/organisation/accounts"

acc_payload = """
{
	"data": {
		"id": "%s",
		"organisation_id": "%s",
		"type": "accounts",
		"attributes": {
			"bank_id": "%s",
			"bank_id_code": "GBDSC",
			"bic": "%s",
			"country": "GB",
			"base_currency": "GBP",
			"account_number": "%s",
			"customer_id": "%s"
		}
	}
}
""" % (acc_id, organisation_id, bank_id, bic, account_number, customer_id)

acc_headers = {
    'authorization': "bearer %s" % auth_token,
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

account = requests.request("POST", acc_url, data=acc_payload, headers=acc_headers)

print(account.text)