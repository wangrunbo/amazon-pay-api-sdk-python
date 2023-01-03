# Amazon Pay API SDK (Python)

Amazon Pay Integration.

Please note this is a **Non-Official** Amazon Pay Python SDK and can only be used for API calls to the
**_pay-api.amazon.com|eu|jp_** endpoint.

For more details about the api, please check
the [Official Documentation for developers](https://developer.amazon.com/docs/amazon-pay/intro.html).

## Requirements

* Python 3.x
* requests >= 2.28.1
* pycryptodome >= 3.16.0

## SDK Installation

Use PyPI to install the latest release of the SDK:

```
pip install AmazonPayClient
```

## Configuration

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='jp',
    sandbox=True
)
```

If you have created environment specific keys (i.e. Public Key Starts with LIVE or SANDBOX) in Seller Central, then use
those PublicKeyId & PrivateKey. In this case, there is no need to pass the sandbox parameter to the configuration.

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='jp',
)
```

# Versioning

The pay-api.amazon.com|eu|jp endpoint uses versioning to allow future updates. The major version of this SDK will stay
aligned with the API version of the endpoint.

If you have downloaded version 2.x.y of this SDK, the API version would be "v2".

If you need to use a "v1" version of Amazon Pay API,
seek [Official Documentation](https://developer.amazon.com/docs/amazon-pay/intro.html) for help.

# Convenience Functions (Overview)

Make use of the built-in convenience functions to easily make API calls. Scroll down further to see example code
snippets.

When using the convenience functions, the request payload will be signed using the provided private key, and a HTTPS
request is made to the correct regional endpoint.

## Alexa Delivery Trackers API

[Delivery Trackers API Guide](https://developer.amazon.com/docs/amazon-pay-api-v2/delivery-tracker.html)

* Create Delivery Tracker - **create_delivery_tracker**(body: dict)

## Amazon Checkout v2 API

[API Integration Guide](https://amazonpaycheckoutintegrationguide.s3.amazonaws.com/amazon-pay-api-v2/introduction.html)

### Buyer

[Buyer API Guide](https://developer.amazon.com/docs/amazon-pay-api-v2/buyer.html)

* Get Buyer - **get_buyer**(buyer_token: str)

### Checkout Session

[Checkout Session API Guide](https://developer.amazon.com/docs/amazon-pay-api-v2/checkout-session.html)

* Create Checkout Session - **create_checkout_session**(body: dict)
* Get Checkout Session - **get_checkout_session**(checkout_session_id: str)
* Update Checkout Session - **update_checkout_session**(checkout_session_id: str, body: dict)
* Complete Checkout Session - **complete_checkout_session**(checkout_session_id: str, body: dict)

### Charge Permission

[Charge Permission API Guide](https://developer.amazon.com/docs/amazon-pay-api-v2/charge-permission.html)

* Get Charge Permission - **get_charge_permission**(charge_permission_id: str)
* Update Charge Permission - **update_charge_permission**(charge_permission_id: str, body: dict)
* Close Charge Permission - **close_charge_permission**(charge_permission_id: str, body: dict)

### Charge

* Create Charge - **create_charge**(body: dict)
* Get Charge - **get_charge**(charge_id: str)
* Capture - **capture_charge**(charge_id: str, body: dict)
* Cancel Charge - **cancel_charge**(charge_id: str, body: dict)

### Refund

* Create Refund - **create_refund**(body: dict)
* Get Refund - **get_refund**(refund_id: str)

# Convenience Functions Code Samples

## Alexa Delivery Notifications

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=False
)

body = {
    'amazonOrderReferenceId': 'P00-0000000-0000000',
    'deliveryDetails': [
        {
            'carrierCode': 'UPS',
            'trackingNumber': '1Z999AA10123456784'
        }
    ]
}

response = client.create_delivery_tracker(body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Create Checkout Session

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

body = {
    'webCheckoutDetails': {
        'checkoutReviewReturnUrl': 'https://localhost/store/checkout_review',
        'checkoutResultReturnUrl': 'https://localhost/store/checkout_result'
    },
    'storeId': 'YOUR_STORE_ID'
}

response = client.create_checkout_session(body)

if response.status_code == 201:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Get Checkout Session

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

checkout_session_id = '00000000-0000-0000-0000-000000000000'

response = client.get_checkout_session(checkout_session_id)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Update Checkout Session

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

checkout_session_id = '00000000-0000-0000-0000-000000000000'
body = {
    'paymentDetails': {
        'chargeAmount': {
            'amount': '100',
            'currencyCode': 'JPY'
        }
    }
}

response = client.update_checkout_session(checkout_session_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Complete Checkout Session

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

checkout_session_id = '00000000-0000-0000-0000-000000000000'
body = {
    'chargeAmount': {
        'amount': '100',
        'currencyCode': 'JPY'
    }
}

response = client.complete_checkout_session(checkout_session_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Get Charge Permission

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_permission_id = 'S00-0000000-0000000'

response = client.get_charge_permission(charge_permission_id)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Update Charge Permission

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_permission_id = 'S00-0000000-0000000'
body = {
    'merchantMetadata': {
        'merchantReferenceId': '00-00-000000-00',
        'merchantStoreName': 'Test Store',
        'noteToBuyer': 'Some Note to buyer',
        'customInformation': 'Custom Information'
    }
}

response = client.update_charge_permission(charge_permission_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Close Charge Permission

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_permission_id = 'S00-0000000-0000000'
body = {
    'closureReason': 'No more charges required',
    'cancelPendingCharges': False
}

response = client.close_charge_permission(charge_permission_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Create Charge

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

body = {
    'chargePermissionId': 'S00-0000000-0000000',
    'chargeAmount': {
        'amount': '100',
        'currencyCode': 'JPY'
    },
    'captureNow': True
}

response = client.create_charge(body)

if response.status_code == 201:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Get Charge

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_id = 'S00-0000000-0000000-C000000'

response = client.get_charge(charge_id)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Capture Charge

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_id = 'S00-0000000-0000000-C000000'
body = {
    'captureAmount': {
        'amount': '100',
        'currencyCode': 'JPY'
    }
}

response = client.capture_charge(charge_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Cancel Charge

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

charge_id = 'S00-0000000-0000000-C000000'
body = {
    'cancellationReason': 'REASON DESCRIPTION'
}

response = client.cancel_charge(charge_id, body)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Create Refund

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

body = {
    'chargeId': 'S00-0000000-0000000-C000000',
    'refundAmount': {
        'amount': '100',
        'currencyCode': 'JPY'
    },
}

response = client.create_refund(body)

if response.status_code == 201:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

## Amazon Checkout v2 - Get Refund

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

refund_id = 'S00-0000000-0000000-R000000'

response = client.get_refund(refund_id)

if response.status_code == 200:
    # success
    result = response.json()
    print(result)
else:
    # check the error
    print('Status Code: ' + str(response.status_code) + '\n' + 'Content: ' + response.content.decode(encoding='utf-8') + '\n')
```

# Generate Button Signature (helper function)

The signatures generated by this helper function are only valid for the Checkout v2 front-end buttons. Unlike API
signing, no timestamps are involved, so the result of this function can be considered a static signature that can safely
be placed in your website JS source files and used repeatedly (as long as your payload does not change).

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

payload = '{"webCheckoutDetails": {"checkoutResultReturnUrl": "https://localhost/store/checkout_result", "checkoutMode": "ProcessOrder"}, "chargePermissionType": "OneTime", "paymentDetails": {"paymentIntent": "Confirm", "chargeAmount": {"amount": "100", "currencyCode": "JPY"}}, "storeId": "YOUR_STORE_ID"}'

signature = client.generate_button_signature(payload)
```

You can also use a _dict_ as your payload. But make sure the `json.dumps(payload)` result matches the one you are using
in your button, such as spaces etc.

```python
from AmazonPay import Client

client = Client(
    public_key_id='YOUR_PUBLIC_KEY_ID',
    private_key='keys/private.pem',
    region='us',
    sandbox=True
)

payload = {
    'webCheckoutDetails': {
        'checkoutResultReturnUrl': 'https://localhost/store/checkout_result',
        'checkoutMode': 'ProcessOrder'
    },
    'chargePermissionType': 'OneTime',
    'paymentDetails': {
        'paymentIntent': 'Confirm',
        'chargeAmount': {
            'amount': '100',
            'currencyCode': 'JPY'
        }
    },
    'storeId': 'YOUR_STORE_ID'
}

signature = client.generate_button_signature(payload)
```