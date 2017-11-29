#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Creating Submission Resource Snippet ###
# Submits a payment.

import uuid, requests

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
    }

submission = requests.request("POST", submission_url, data=submission_payload, headers=submission_headers)

print(submission.text)