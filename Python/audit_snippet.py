#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Fetching Submission Audit Entries Snippet
# Fetch an audit resource detailing status updates of a submission resource.

import requests
from pprint import pprint 	# pretty print to improve readability of JSON structures

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