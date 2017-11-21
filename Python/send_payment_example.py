import math, random, requests, time, uuid

### Replace these variables with your own data! ###
client_id = 'YOUR CLIENT ID HERE'
client_secret = 'YOUR CLIENT SECRET HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
bank_id = 'YOUR BANK ID HERE'
callback_url = "YOUR CALLBACK URL HERE"

### Generate IDs for all calls ###
subscription_id = uuid.uuid4()
payment_id = uuid.uuid4()
submission_id = uuid.uuid4()
print("Payment ID: %s" % payment_id)
print("Subscription ID: %s" % subscription_id)
print("Submission ID: %s" % submission_id)

base_url = 'https://api.test.form3.tech'

### Authenticate ###
auth_payload = "grant_type=client_credentials"
auth_url = 'https://api.tabla.env.form3.tech/v1/oauth2/token'
auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
auth_request = requests.auth.HTTPBasicAuth(client_id, client_secret)

auth = requests.request('post', auth_url, data=auth_payload, auth=auth_request, headers=auth_headers)
print(auth.content)

auth_token = auth.json().get('access_token')
print("Bearer token: %s" % auth_token)

### Create Payment Submission Subscription ###
subscription_url = "%s/v1/notification/subscriptions" % base_url

subscription_payload = """
{
	"data": {
		"type": "subscriptions",
		"id": "%s",
		"organisation_id": "%s",
		"attributes": {
			"callback_uri": "%s",
			"callback_transport": "http",
			"event_type": "updated",
			"record_type": "payment_submissions"
		}
	}
}
""" % (subscription_id, organisation_id, callback_url)

subscription_headers = {
    'authorization': "bearer %s" % auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "02efa25f-26cb-df8e-ca44-7a6d4051a023"
    }

subscription = requests.request("POST", subscription_url, data=subscription_payload, headers=subscription_headers)
print(subscription.text)


### Creating Payment Resource ###
scheme_transaction_id = str(int(math.floor((1 + random.random()) * 100000000000000000)))
payment_url = "%s/v1/transaction/payments" % base_url
payment_payload = """
{
	"data": {
		"type": "payments",
		"id": "%s",
		"version": 0,
		"organisation_id": "%s",
		"attributes": {
			"amount": "13.00",
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
				"account_number": "87654321",
				"account_number_code": "BBAN",
				"account_with": {
					"bank_id": "%s",
					"bank_id_code": "GBDSC"
				}
			},
			"scheme_transaction_id": "%s",
			"processing_date": "%s",
			"reference": "Something",
			"scheme_payment_sub_type": "TelephoneBanking",
			"scheme_payment_type": "ImmediatePayment"
		}
	}
}
""" % (payment_id, organisation_id, bank_id, scheme_transaction_id, time.strftime("%Y-%m-%d"))

payment_headers = {
    'authorization': "bearer " + auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "3323f800-6191-f13b-4c4d-f62179caa978"
    }

payment = requests.request("POST", payment_url, data=payment_payload, headers=payment_headers)
print(payment.text)

### Creating Submission ###
submission_url = "%s/v1/transaction/payments/%s/submissions" % (base_url, payment_id)

submission_payload = """
{
	"data": {
		"id": "%s",
		"type": "paymentsubmissions",
		"organisation_id": "%s"
	}
}
""" % (submission_id, organisation_id)

submission_headers = {
    'authorization': "bearer %s" % auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "f09ad285-4223-ef05-0d4c-bc1048546a82"
    }

submission = requests.request("POST", submission_url, data=submission_payload, headers=submission_headers)

print(submission.text)


### Query submission resource ###
get_subm_url = "%s/v1/transaction/payments/%s/submissions/%s" % (base_url, payment_id, submission_id)

get_subm_headers = {
    'authorization': "bearer %s" % auth_token,
    'cache-control': "no-cache",
    'postman-token': "ab4adba7-f0fb-4707-d1e1-437ea32d81a8"
    }

get_subm = requests.request("GET", get_subm_url, headers=get_subm_headers)

print(get_subm.text)


### Clean Up Subscription ###
del_subm_url = "%s/v1/notification/subscriptions/%s" % (base_url, subscription_id)

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