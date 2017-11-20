### Creating Submission Subscription Snippet
# Creates a webhook subscription for payment submission

import requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
callback_url = 'YOUR CALLBACK URL HERE'

# Generate IDs
subscription_id = uuid.uuid4()
print("Subscription ID: %s" % subscription_id)

subscription_url = "https://api.tabla.env.form3.tech/v1/notification/subscriptions"
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