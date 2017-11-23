# Guide: Making a Payment

In this guide you will learn how to use the Form3 Payments API to make a payment through Faster Payments Service (FPS). The guide covers the following steps:
- Sending the payment
- Tracking the payment progress manually
- Tracking the payment progress automatically using subscriptions

Each step is illustrated with Python code snippets, so you can execute each step as you read along. The snippets are ready-to-run programs and work in Python's interactive console.

## Introduction

Before diving into the implementation, let's have a quick look at what it means to send a payment from one bank account to another.

A transfer of funds usually requires a bank and an account with that bank on the sender side, as well as the receiving side.

The sending bank and the receiving bank are identified using a bank ID. The format of this ID depends on the country the bank is registered in. In the UK it is a 6-digit number that denotes the bank and the branch of the bank. The account is identified by the account number. 

To make a payment, the sending party creates a payment resource that specifies all important information about the payment: who sends it, who receives it, the amount, the currency, and so forth.

The sending party then submits the payment. The banking scheme performs several steps of validation and routes the payment to the receiving party. On its way through the system, the status of the payment submission changes until its delivery is either acknowledged or declined by the receiving bank.



![Sending_Payment_Diagram](/Sending_Payment_Diagram.JPG)



## Prerequisites
Before you start, make sure you have the following things ready to go:
- Your API credentials and an organisation ID. Contact Form3 to obtain them.
- Register your UK sortcodes and BICs with Form3.
- Sign up for Form3's scheme simulator for FPS payments. This is a sandbox environment that you can use to simulate transactions in order to test your application.
- If you want to run the Python code snippets, make sure you have [Python 2.7](https://www.python.org/downloads/) installed. You also need the requests package. The easiest way is to install it through [Pip](https://docs.python.org/2.7/installing/index.html): `pip install requests`


## Get a Bearer Token

As a first step, you need to obtain a bearer token using your client ID and your client secret. This token will be used in the other API calls to authenticate yourself to the Form3 server.

```python
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
```

## Create the Payment

To make a payment, you need to complete two steps. First create a payment resource to define the payment parameters, then send it by creating a payment submission resource. This payment submission is also used later to track the status of your payment.

### Create the Payment Resource


Create a payment resource for the payment you are going to send. It contains all information required to process the payment. 

The key parameters that you need to provide are:

- `amount`: The amount to be paid
- `currency`: The currency code of the currency for the amount
- `debtor` and `beneficiary`: Data structures containing the account information of the sending and the receiving party.


#### Debtor and Beneficiary Data

To identify the sending and receiving parties of the payment, you need to provide an `account_name`, the `account_number`, the `account_number_code`, as well as the `bank_id` and `bank_id_code` for the bank the account is registered with. 

In this example, use your UK sortcode for the sending party's `bank_id`. 

The `bank_id_code ` attribute denotes the type of the `bank_id`. Since only domestic UK accounts are used in this example, the `bank_id_code` is preset as `GBDSC`.

A detailed description of each field of the payment resource is available in the [API documentation](http://draft-api-docs.form3.tech/?http#create92).

```python
import math, random, requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
bank_id = 'YOUR UK SORTCODE HERE'

# Generate IDs
payment_id = uuid.uuid4()
print("Payment ID: %s" % payment_id)

payment_url = "https://api.test.form3.tech/v1/transaction/payments"
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
            "processing_date": "%s",
            "reference": "Something",
            "scheme_payment_sub_type": "TelephoneBanking",
            "scheme_payment_type": "ImmediatePayment"
        }
    }
}
""" % (payment_id, organisation_id, bank_id, time.strftime("%Y-%m-%d"))

payment_headers = {
    'authorization': "bearer " + auth_token,
    'accept': "application/json",
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

payment = requests.request("POST", payment_url, data=payment_payload, headers=payment_headers)
print(payment.text)
```

### Create the Submission Resource

The next step is to send the payment by creating a payment submission resource. Note that you have to provide the payment ID in the call.

```python
import requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
payment_id = 'A VALID PAYMENT ID HERE'

# Generate IDs
submission_id = uuid.uuid4()
print("Submission ID: %s" % submission_id)

submission_url = "https://api.test.form3.tech/v1/transaction/payments/%s/submissions" % payment_id
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
```

And just like that, your payment is on its way!

## Track the Payment Manually

There are several ways to monitor your payment and track it on its way through the system. The easiest one is to query the submission resource that you created above:

`GET /transaction/payments/{payment_id}/submissions/{submission_id}`

Note that the submission resource is identified using the `payment_id` and the `submissions_id`.

The response contains the current status of the payment in an attribute called `status`. If the payment has been successful, the status attribute says `delivery_confirmed`. Failed payments are denoted with a status attribute value `delivery_failed`. In this case, the attribute `status_reason` contains further information about why the payment failed. 

A detailed description of all possible values of the status attribute and their meaning is available in the [API documentation](http://draft-api-docs.form3.tech/?http#payment-submission-status).

```python
import requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
payment_id = 'A VALID PAYMENT ID HERE'
submission_id = 'A VALID SUBMISSION ID HERE'

get_subm_url = "https://api.test.form3.tech/v1/transaction/payments/%s/submissions/%s" % (payment_id, submission_id)
get_subm_headers = {
    'authorization': "bearer %s" % auth_token,
    'cache-control': "no-cache",
    'postman-token': "ab4adba7-f0fb-4707-d1e1-437ea32d81a8"
    }

get_subm = requests.request("GET", get_subm_url, headers=get_subm_headers)

print(get_subm.text)
```

## Track the Payment using Subscriptions

Another way of tracking your payment is to use subscriptions. You can subscribe to certain events and automatically be notified when they occur. 

The Form3 API supports [Amazon SQS](https://aws.amazon.com/sqs/) and webhook URLs to notify subscribers when an event occurs.

<aside class="notice">
Using Amazon SQS is recommended, since it is a managed, highly-available solution and less error-prone than webhooks. For the sake of simplicity, however, this guide uses a webhook to demonstrate the subscription API.</aside>

### Create a Subscription using Webhooks

In order to subscribe to an event via webhook, you need to provide the API with a callback URL. This needs to be a public URL that the API can call and notify you whenever the event has occured.

### Using RequestBin to create a public URL

The easiest way to set up a public URL for testing is to use [RequestBin](https://requestb.in). With RequestBin you can set up a public URL and see inspect the calls that are made to it. On the RequestBin website, simply click the "Create a RequestBin" button. Your public callback URL is displayed at the top right of the page.

### Create the Subscription Resource


To subscribe to an event, create a subscription resource. To be notified through a webhook, choose `callback_transport` to be `http`. The parameter `callback_uri` needs to contain your ngrok URL.

The attribute `record_type` contains the type of event you want to subscribe to. In this case, choose `payment_submissions`. 

A full list of event types is available in the [API documentation](http://draft-api-docs.form3.tech/?http#payment-events).

```python
import requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
callback_url = 'YOUR CALLBACK URL HERE'

# Generate IDs
subscription_id = uuid.uuid4()
print("Subscription ID: %s" % subscription_id)

subscription_url = "https://api.test.form3.tech/v1/notification/subscriptions"
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
```

To test the webhook, repeat the steps of creating a payment and a submission resource. Visit the RequestBin page to see the callbacks to your URL. If everything worked, the message body will contain `"status":"delivery_confirmed"`.


## Track a Resource a Resource using Audits

Another way to track your payment is using audits. Each time something happens in the system and a resource changes its state, an audit entry is created to document it. To monitor the status of an outgoing payment, the best resource to track is the submission resource that was created above to submit the payment:

`GET /audit/entries/payment_submissions/{submission_id}`

The response contains a number of `AuditEntry` elements. Each entry contains an `after_data` section with a `status` attribute. This attribute denotes the status of the resource after the event that the `AuditEntry` element describes.

A typical successful payment goes through the following stages:

- *accepted*
- *validation_pending*
- *limit_check_pending*
- *released_to_gateway*
- *delivery_confirmed*

In case the processing of the payment resource fails at some point in the system, the status update trail would contain an error message and terminate with the status *delivery_failed*.

A full list of statuses can be found in the [API documentation](http://draft-api-docs.form3.tech/))

```python
import requests
from pprint import pprint

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
submission_id = 'A VALID SUBMISSION ID HERE'

audit_url = "https://api.test.form3.tech/v1/audit/entries/payment_submissions/%s" % submission_id

audit_headers = {
    'authorization': "bearer %s" % auth_token,
    'cache-control': "no-cache"
    }

audit = requests.request("GET", audit_url, headers=audit_headers)
pprint(audit.json())
```



That's it, you now know how to make a payment using the Form3 Payments API. Continue to the next guide to learn how to receive a payment.