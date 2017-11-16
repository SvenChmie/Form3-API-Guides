# Guide: Making a Payment

_(Note: Are there any specific steps required for different payment schemes (SWIFT etc.)? Do the steps in this guide work the same for any scheme? Should be mentioned somehow)_

In this guide you will learn how to use the Form3 Payments API to make a payment. The guide covers the following steps:
- Send the payment
- Track the payment progress manually
- Track the payment progress automatically using subscriptions

## Prerequisites:
Before you start, make sure you have the following things ready to go:
- API credentials. Contact your Form3 contact to obtain your credentials. _(Note: Better name for this role? Who do they have to contact?)_
- Register your bank ID and BIC with Form3
- Sign up for Form3's scheme simulator. This is a sandbox environment that you can use to simulate transactions in order to test your application. _(Note: in the API this is called "payment simulator". Which term should we use?)_


## Get a Bearer Token

As a first step, you need to obtain a bearer token using your API credentials. This token will be used to authenticate yourself to the Form3 server.

_(Note: Should we elaborate on how to do that?)_

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

```json
Code for payment resource creation here!
```
Upon success, the call returns with a payment ID that you'll need below to send the payment.

A detailed description of each field of the payment resource is available in the [API documentation](http://draft-api-docs.form3.tech/?http#create92).



### Create the Submission Resource

The next step is to send the payment by creating a payment submission resource. Note that you have to provide the payment ID in the call.

```json
Code for submission resource here!
```



## Track the Payment Manually

...



## Track the Payment using Subscriptions

...





