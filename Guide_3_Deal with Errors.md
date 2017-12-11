
# Deal with Errors Correctly

Sending and receiving payments with the Form3 Payments API is quick and simple, but sometimes a payment submission fails for one reason or another.

This tutorial takes a look at different errors that can occur during a payment submission and explains how they can be diagnosed. This tutorial covers the following topics:

- What happens if payment data is incomplete
- What happens if the receiving account data is incorrect

## Invalid Payment Data

If an outbound payment is created with invalid or incomplete data, it cannot be processed correctly.

Depending on the kind of error, the server will respond differently. In case the request is made with incorrect JSON syntax, the server will send a response with the status _400 Bad Request_.

If the syntax is correct, the creation of a payment resource will be successful. The payment is then sent by creating a submission resource. Invalid data will cause the submission to fail, resulting in a "delivery failed" status. 

To check the status of the submission, you can use the GET method for the submission resource itself, you can use audits to see the entire history of the resource, or you can subscribe to the creation event of submission resources to receive a notification whenever a new submission resource is created.

Using either of these methods, you can read the `status` attribute of the submission. If the submission has failed, the `status` will say `delivery_failed`. In this case, the `status_reason` attribute provides further information about the error. If, for example, the `amount` attribute in the payment resource was missing, the status reason says _"attributes.amount:may not be null. Value passed was null"_. 

## Invalid Receiving Account Data

Another problem can occur if all the attributes in the payment resource are correct, but the account number or the sortcode of the recipient are invalid.

Since the payment is formally correct, it is submitted without an error. In case the sortcode is invalid, the transaction scheme will notice the invalid code and return with an error.

An invalid receiver bank account will be noticed by the receiving bank. In case a non-existing account number is specified, the receiving bank will reject the inbound payment and the error message is transferred back to the sender.

In both cases, the `status` attribute of the submission resource will say _"delivery_failed"_. The `status_reason` attribute provides an error message. If the payment is sent using Faster Payment Service (FPS) scheme, it says _"beneficiary-sort-code/account-number-unknown"_. Other payment schemes might provide different error messages.

A full list of FPS payment return codes can be found in the [API documentation](/api.html#payment-return-codes).