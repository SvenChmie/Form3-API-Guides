#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Creating Payment Resource Snippet ###
# Creates a payment resource for an UK FPS payment.

import math, uuid, random, requests

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