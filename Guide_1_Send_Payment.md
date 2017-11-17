# Guide: Making a Payment

_**(Note: Are there any specific steps required for different payment schemes (SWIFT etc.)? Do the steps in this guide work the same for any scheme? Should be mentioned somehow)**_

In this guide you will learn how to use the Form3 Payments API to make a payment. The guide covers the following steps:
- Send the payment
- Track the payment progress manually
- Track the payment progress automatically using subscriptions

Each step is illustrated with Python code snippets, so you can execute each step as you read along. The snippets are ready-to-run programs and work in Python's interactive console.

## Prerequisites:
Before you start, make sure you have the following things ready to go:
- API credentials. Contact your Form3 contact to obtain your credentials. _**(Note: Better name for this role? Who do they have to contact?)**_
- Register your bank ID and BIC with Form3
- Sign up for Form3's scheme simulator. This is a sandbox environment that you can use to simulate transactions in order to test your application. _**(Note: in the API this is called "payment simulator". Which term should we use?)**_
- If you want to run the Python code snippets, make sure you have [Python 2.7](https://www.python.org/downloads/) installed. You also need the requests package. The easiest way is to install it through [Pip](https://docs.python.org/2.7/installing/index.html): `pip install requests`


## Get a Bearer Token

```python
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
```

As a first step, you need to obtain a bearer token using your client ID and your client secret. This token will be used in the other API calls to authenticate yourself to the Form3 server.

## Create the Payment

To make a payment, you need to complete two steps. First create a payment resource to define the payment parameters, then send it by creating a payment submission resource. This payment submission is also used later to track the status of your payment.

### Create the Payment Resource

```json
Code for payment resource creation here!
```

Create a payment resource for the payment you are going to send. It contains all information required to process the payment. 

The key parameters that you need to provide are:

- `amount`: The amount to be paid
- `currency`: The currency code of the currency for the amount
- `debtor` and `beneficiary`: Data structures containing the account information of the sending and the receiving party.


#### Debtor and Beneficiary Data

To identify the sending and receiving parties of the payment, you need to provide an `account_name`, the `account_number`, the `account_number_code`, as well as the `bank_id` and `bank_id_code` for the bank the account is registered with.

Upon success, the call returns with a payment ID that you'll need below to send the payment.

A detailed description of each field of the payment resource is available in the [API documentation](http://draft-api-docs.form3.tech/?http#create92).



### Create the Submission Resource

```json
Code for submission resource here!
```

The next step is to send the payment by creating a payment submission resource. Note that you have to provide the payment ID in the call.

And just like that, your payment is on its way!

## Track the Payment Manually

_**(Question: Should Audits be mentioned here? Since it said in the email that audits are not recommended and this is a getting started guide, maybe it's more straightforward and less confusing not to mention it?)**_

There are several ways to monitor your payment and track it on its way through the system. The easiest one is to query the submission resource that you created above:

`GET /transaction/payments/{payment_id}/submissions/{submission_id}`

Note that the submission resource is identified using the `payment_id` and the `submissions_id`.

The response contains the current status of the payment in an attribute called `status`. If the payment has been successful, the status attribute says `delivery_confirmed`. Failed payments are denoted with a status attribute value `delivery_failed`. In this case, the attribute `status_reason` contains further information about why the payment failed. 

A detailed description of all possible values of the status attribute and their meaning is available in the [API documentation](http://draft-api-docs.form3.tech/?http#payment-submission-status).

## Track the Payment using Subscriptions

Another way of tracking your payment is to use subscriptions. You can subscribe to certain events and automatically be notified when they occur. 

The Form3 API supports [Amazon SQS](https://aws.amazon.com/sqs/) and webhook URLs to notify subscribers when an event occurs.

**_(Note: I've used Slate HTML syntax below, although you can't see it on GitHub, because they strips it before displaying. We'll use Slate to display this guide, right?)_**

<aside class="notice">
Using Amazon SQS is recommended, as it is a managed, highly-available solution and less error-prone than webhooks. For the sake of simplicity, however, this guide uses a webhook to demonstrate the subscription API.</aside>

### Create a Subscription using Webhooks

In order to subscribe to an event via webhook, you need to provide the API with a callback URL. This needs to be a public URL that the API can call and notify you whenever the event has occured.

### Using ngrok to create a public URL

The easiest way to set up a public URL for testing is to use [ngrok](https://ngrok.com/). With ngrok you can create a tunnel to expose a webserver running on your local machine to the public Internet. Follow the steps in the [ngrok documentation](https://ngrok.com/docs/2) to set up the tunnel.

_**(Note: This doesn't contain any information about the type of server that has to run on the localhost. Should we provide any info on that?)**_

### Create the Subscription Resource

```json
Subscription Resource Example Code here!
```

To subscribe to an event, create a subscription resource. To be notified through a webhook, choose `callback_transport` to be `http`. The parameter `callback_uri` needs to contain your ngrok URL.

The attribute `record_type` contains the type of event you want to subscribe to. In this case, choose `PaymentSubmission`. 

A full list of event types is available in the API documentation. **_(Note: Where? I couldn't find one...)_**

To test the webhook, create another subscription resource. If everything is set up correctly, the webhook will trigger your local server and notify you about the payment.

That's it, you now know how to make a payment using the Form3 Payments API. Continue to the next guide to learn how to receive a payment. 








