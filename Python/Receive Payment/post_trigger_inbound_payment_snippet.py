#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Triggering an Inbound Payment Snippet ###
# Creates a payment resource and a submission resource in order to trigger an inbound payment.
# Sending amounts of 600.00 trigger an immediate inbound payment.

import uuid, requests, times

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