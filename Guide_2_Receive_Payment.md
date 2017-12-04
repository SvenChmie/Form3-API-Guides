# Guide: Receiving a Payment

In this tutorial, you will learn how to receive a payment from a third party using the Form3 Payments API. The following steps will be covered:

- Creating an account

- Triggering an inbound payment

- Tracking the payment admission both manually and automatically

Each step is illustrated with Python code snippets, so you can execute each step as you read along. The snippets are ready-to-run programs and work in Python's interactive console.

## Introduction

In order to better understand how to receive a payment, let's take a look at what happens when a third party sends a payment to an account that you manage.

A transfer of funds requires a bank and an account with that bank on the sender side, as well as the receiving side.

The sending bank and the receiving bank are identified using a bank ID. The format of this ID depends on the country the bank is registered in. In the UK it is a 6-digit number that denotes the bank and the branch of the bank. The account is identified by the account number.

When a payment is sent, the sending party creates a payment resource that specifies all important information about the payment: who sends it, who receives it, the amount, the currency, and so forth.

A payment admission resource is created when the payment reaches the receiving side. This admission resource represents the transaction on the receiving side and contains the status of the admission, as well as a description of an error in case one occurred.

If the payment admission was successful and the funds have been added to the beneficiary bank account, the receiving bank sends an acknowledge message to the sending bank and the transfer is complete.

![Receiving_Payment_Diagram](Images\Receiving_Payment_Diagram.JPG)



## Prerequisites

It  is recommended that you complete the previous tutorial about sending a payment before reading this one. 

Before you start, make sure you have the following things ready to go:

- Your API credentials and an organisation ID. Contact Form3 to obtain them.
- Register your UK sortcodes and BICs with Form3.
- Sign up for Form3's scheme simulator for FPS payments. This is a sandbox environment that you can use to simulate transactions in order to test your application.
- If you want to run the Python code snippets, make sure you have [Python 2.7](https://www.python.org/downloads/) installed. You also need the requests package. The easiest way is to install it through [Pip](https://docs.python.org/2.7/installing/index.html): `pip install requests`

## Get a Bearer Token

As a first step, you need to obtain a bearer token using your client ID and your client secret. This token will be used in the other API calls to authenticate yourself to the Form3 server.

> Fetch the bearer token for authentication

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

##  Create an Account

To receive a payment on a bank account, that account needs to be registered with Form3. In order to register a bank account, an account resource is created. To create an account resource, the following data is required:

- A `bank_id` and `bank_id_code`. For the Faster Payments Service (FPS), the `bank_id` is a 6-digit number and the code is `GBDSC`.
- The bank's BIC code. You need to register your `bic` with Form3 before you can create an account.
- The country and base currency. Since FPS is a domestic scheme, the country is `GB` and the currency is `GBP`. 
- A customer ID. This attribute does not have form constraints.

<aside class="notice">A different option to create an account is to enable **automatic account creation**. In that case, an account resource is automatically created when an inbound payment arrives with an unknown account number. Contact Form3 to see if automatic account creation can be enabled for your company.</aside>

```python
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
    'authorization': "bearer %s" % auth_token
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

account = requests.request("POST", acc_url, data=acc_payload, headers=acc_headers)

print(account.text)
```

## Create a Subscription

The easiest way to track inbound payments is to set up a subscription to the `payment_admissions` event. That way, you are automatically notified when the event occurs.

The Form3 API supports [Amazon SQS](https://aws.amazon.com/sqs/) and webhook URLs to notify subscribers.

<aside class="notice">
Using Amazon SQS is recommended since it is a managed, highly-available solution and less error-prone than webhooks. For the sake of simplicity, however, this guide uses a webhook to demonstrate the subscription API.</aside>

**Create a Subscription using Webhooks**

In order to subscribe to an event via webhook, you need to provide the API with a callback URL. This needs to be a public URL that the API can call and notify you whenever the event has occurred.

**Using RequestBin to create a public URL**

The easiest way to set up a public URL for testing is to use [RequestBin](https://requestb.in). With RequestBin, you can set up a public URL and inspect the calls that are made to it. On the RequestBin website, simply click the "Create a RequestBin" button. Your public callback URL is displayed at the top right of the page.

**Create the Subscription Resource**

To subscribe to an event, create a subscription resource. To be notified through a webhook, choose `callback_transport` to be `http`. The parameter `callback_uri` needs to contain your callback URL.

The `event_type` attribute denotes the type of event. For this example, it should set to `created`, since your are listening for the creation of a resource. The attribute `record_type` contains the resource you want to subscribe to. To track admissions of inbound payments, choose `payment_admissions`.

A full list of event types and resource names is available in the [API documentation](/api.html#payment-events).

```python
import uuid, requests

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
```

## Trigger an Inbound Payment

For learning and testing purposes, an inbound to an account can be triggered using the scheme simulator. Sending an outbound payment with an `amount` of 600.00 through the simulator will trigger an immediate inbound payment with the same amount back to sending account.

To create an outbound payment, first create a payment resource and then a submission resource to send the payment. See our[ Send a Payment tutorial](???) for details how to create these resources.

For the debtor party of the outgoing payment, use the account you created above by specifying the `account_number`, and your `bank_id`. The `account_name` parameter is required, but can be any name you like. 

The `account_number_code` and `bank_id_code` are fixed due to the payment scheme that is used in this example.

```python
import uuid, requests, time

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
organisation_id = 'YOUR ORGANISATION ID HERE'
bank_id = 'YOUR UK SORTCODE HERE'
account_number = 'A VALID ACCOUNT NUMBER HERE'

# Generate IDs
payment_id = uuid.uuid4()
submission_id = uuid.uuid4()
print("Payment ID: %s" % payment_id)
print("Submission ID: %s" % submission_id)

# Base URL
base_url = "https://api.test.form3.tech/v1"

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
```



## Track the Payment Admission

The outbound payment has triggered an immediate inbound payment to the debtor account of the outgoing payment.

Take a look at your RequestBin that you used earlier to subscribe to the creation of payment admission resources. You should see a notification for a new admission resource. Scroll through the payload to find the `status` attribute. If everything worked, it says `confirmed`, while the `status_reason` has the value `accepted`.

That's it, you have successfully received a payment and tracked it using the Form3 Payments API.



