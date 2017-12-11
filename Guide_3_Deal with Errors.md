
# Deal with Errors Correctly

Sending and receiving payments with the Form3 Payments API is quick and simple, but sometimes a payment submission fails for one reason or another.

This tutorial takes a look at different errors that can occur during a payment submission and explains how they can be diagnosed. This tutorial covers the following topics:

- What happens if payment data is incomplete
- What happens if the receiving account data is incorrect

## Prerequisites

It is recommended that you complete the previous tutorials about [sending](/tutorial-send-a-payment.html) and [receiving](/tutorial-receive-a-payment.html) a payment before reading this one.

Before you start, make sure you have the following things ready to go:

- Your API credentials and an organisation ID. Contact Form3 to obtain them.
- Register your UK sortcodes and BICs with Form3.
- Sign up for Form3's scheme simulator for FPS payments. This is a sandbox environment that you can use to simulate transactions in order to test your application.
- If you want to run the Python code snippets, make sure you have [Python 2.7](https://www.python.org/downloads/) installed. You also need the requests package. The easiest way is to install it through [Pip](https://docs.python.org/2.7/installing/index.html): `pip install requests`



## Invalid Payment Data

If an outbound payment is created with invalid or incomplete data, it cannot be processed correctly.

Depending on the kind of error, the server will respond differently. In case the request is made with incorrect JSON syntax, the server will send a response with the status _400 Bad Request_.

If the syntax is correct, the creation of a payment resource will be successful. The payment is then sent by creating a submission resource. Invalid data will cause the submission to fail, resulting in a "delivery failed" status. 

To check the status of the submission, you can use the GET method for the submission resource itself, you can use audits to see the entire history of the resource, or you can subscribe to the creation event of submission resources to receive a notification whenever a new submission resource is created.

Using either of these methods, you can read the `status` attribute of the submission. If the submission has failed, the `status` will say `delivery_failed`. In this case, the `status_reason` attribute provides further information about the error. If, for example, the `amount` attribute in the payment resource was missing, the status reason says _"attributes.amount:may not be null. Value passed was null"_.

Python snippet here

> Payment submission fails due to missing amount attribute in the payment resource.

```json
{
    "data": {
        "type": "payment_submissions",
        "id": "9d924d72-fbe7-44be-97e2-5f60a77f9b59",
        "version": 2,
        "organisation_id": "xxx",
        "attributes": {
            "status": "delivery_failed",
            "status_reason": "attributes.amount:may not be null. Value passed was null",
            "submission_datetime": "2017-12-11T15:45:10.887Z"
        },
        "relationships": {
            "payment": {
                "data": [
                    {
                        "type": "payments",
                        "id": "11c324d9-97dc-4420-a004-9cecaa2a5a8a"
                    }
                ]
            }
        }
    }
}
```

## Invalid Receiving Account Data

Another problem can occur if all the attributes in the payment resource are correct, but the account number or the sort code for the recipient are invalid.

Since the payment is formally correct, it is submitted without an error. In case the sort code is invalid, the transaction scheme will notice the invalid code and return with an error.

Likewise, an invalid receiver bank account will be noticed by the receiving bank. In case a non-existing account number is specified, the receiving bank will reject the inbound payment and the error message is transferred back to the sender.

In both cases, the `status` attribute of the submission resource will contain the status _"delivery_failed"_. The `status_reason` attribute provides a more detailed error message. For an unknown account number or invalid sort code, it says _"beneficiary-sort-code/account-number-unknown"_ if the payment scheme is FPS. Other payment schemes might provide different error messages.

A full list of FPS payment return codes can be found in the [API documentation](/api.html#payment-return-codes).

This type of error can be triggered using Form3's scheme simulator. Create a payment with the amount `216.16`. Submitting this payment will result in a failed delivery with the status reason mentioned above.

Python snippet here!

> Payment submission failed due to unknown sort code or account number

```json
{
    "data": {
        "type": "payment_submissions",
        "id": "190d8768-0775-4839-a6c5-73402029e5a3",
        "version": 4,
        "organisation_id": "xxx",
        "attributes": {
            "status": "delivery_failed",
            "scheme_status_code": "1114",
            "status_reason": "beneficiary-sort-code/account-number-unknown",
            "submission_datetime": "2017-12-11T14:59:52.804Z",
            "settlement_date": "2017-12-11",
            "settlement_cycle": 1
        },
        "relationships": {
            "payment": {
                "data": [
                    {
                        "type": "payments",
                        "id": "08ee2634-7c99-4735-91e2-4ec070db2677"
                    }
                ]
            }
        }
    }
}
```