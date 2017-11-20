### Getting Submission Status Snippet
# Get a submission resource to query the payment status.

import requests

### Replace these variables with your own data! ###
auth_token = 'A VALID BEARER TOKEN HERE'
payment_id = 'A VALID PAYMENT ID HERE'
submission_id = 'A VALID SUBMISSION ID HERE'

get_subm_url = "https://api.tabla.env.form3.tech/v1/transaction/payments/%s/submissions/%s" % (payment_id, submission_id)
get_subm_headers = {
    'authorization': "bearer %s" % auth_token,
    'cache-control': "no-cache",
    'postman-token': "ab4adba7-f0fb-4707-d1e1-437ea32d81a8"
    }

get_subm = requests.request("GET", get_subm_url, headers=get_subm_headers)

print(get_subm.text)