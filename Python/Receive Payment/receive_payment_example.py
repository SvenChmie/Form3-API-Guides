#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, time, uuid
from pprint import pprint

### Replace these variables with your own data! ###
client_id = 'YOUR CLIENT ID HERE'
client_secret = 'YOUR CLIENT SECRET HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
bank_id = 'YOUR BANK ID HERE'
bic = 'YOUR BIC HERE'
account_number = 'A VALID ACCOUNT NUMBER HERE'
customer_id =  'A VALID CUSTOMER ID HERE'
callback_url = 'YOUR CALLBACK URL HERE'

### Generate IDs for all calls ###
subscription_id = uuid.uuid4()
payment_id = uuid.uuid4()
submission_id = uuid.uuid4()
acc_id = uuid.uuid4()

print("Payment ID: %s" % payment_id)
print("Subscription ID: %s" % subscription_id)
print("Submission ID: %s" % submission_id)
print("Account ID: %s" % acc_id)

base_url = 'https://api.test.form3.tech/v1'

### Authenticate ###
print("Getting bearer token...")
auth_payload = "grant_type=client_credentials"
auth_url = '%s/oauth2/token' % base_url
auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
auth_request = requests.auth.HTTPBasicAuth(client_id, client_secret)

auth = requests.request('post', auth_url, data=auth_payload, auth=auth_request, headers=auth_headers)
print(auth.content)

auth_token = auth.json().get('access_token')
print("Bearer token: %s" % auth_token)

### Create new account ###
acc_url = "%s/organisation/accounts" % base_url

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

### Create subscription ###
subscription_url = "%s/notification/subscriptions" % base_url
subscription_payload = """
{
	"data": {
		"type": "subscriptions",
		"id": "%s",
		"organisation_id": "%s",
		"attributes": {
			"callback_uri": "%s",
			"callback_transport": "http",
			"event_type": "created",
			"record_type": "payment_admissions"
		}
	}
}
""" % (subscription_id, organisation_id, callback_url)

subscription_headers = {
    'authorization': "bearer %s" % auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

subscription = requests.request("POST", subscription_url, data=subscription_payload, headers=subscription_headers)
print(subscription.text)

### Trigger inbound payment ###
# Create Payment
payment_url = "%s/transaction/payments" % base_url
payment_payload = """
{
    "data": {
        "type": "payments",
        "id": "%s",
        "version": 0,
        "organisation_id": "%s",
        "attributes": {
            "amount": "600.00",
            "beneficiary_party": {
                "account_name": "Mrs Receiving Test",
                "account_number": "71268996",
                "account_number_code": "BBAN",
                "account_with": {
                    "bank_id": "400302",
                    "bank_id_code": "GBDSC"
                }
            },
            "currency": "GBP",
            "debtor_party": {
                "account_name": "Mr Sending Test",
                "account_number": "%s",
                "account_number_code": "BBAN",
                "account_with": {
                    "bank_id": "%s",
                    "bank_id_code": "GBDSC"
                }
            },
            "processing_date": "%s",
            "reference": "Something",
            "scheme_payment_sub_type": "TelephoneBanking",
            "scheme_payment_type": "ImmediatePayment"
        }
    }
}
""" % (payment_id, organisation_id, account_number, bank_id, time.strftime("%Y-%m-%d"))

headers = {
    'authorization': "bearer " + auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

payment = requests.request("POST", payment_url, data=payment_payload, headers=headers)
print(payment.text)

# Create Submission
submission_url = "%s/transaction/payments/%s/submissions" % (base_url, payment_id)
submission_payload = """
{
    "data": {
        "id": "%s",
        "type": "paymentsubmissions",
        "organisation_id": "%s"
    }
}
""" % (submission_id, organisation_id)

submission = requests.request("POST", submission_url, data=submission_payload, headers=headers)

print(submission.text)

### Clean Up Subscription ###
print("Deleting callback subscription...")
del_subm_url = "%s/notification/subscriptions/%s" % (base_url, subscription_id)

querystring = {"version":"0"}

del_subm_headers = {
    'authorization': "bearer %s" % auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "c155066c-0869-8947-aa37-c8fbe281fb96"
    }

del_subm = requests.request("DELETE", del_subm_url, headers=del_subm_headers, params=querystring)

print(del_subm.text)