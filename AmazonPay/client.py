import datetime
import base64
import uuid
import json
import urllib.parse

import requests
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

AMAZON_SIGNATURE_ALGORITHM = 'AMZN-PAY-RSASSA-PSS'


class Client:

    def __init__(self, public_key_id=None, private_key=None, region=None, sandbox=False):
        """
        Amazon Pay Client
        All parameters can be set later using `setup` function
        :param str public_key_id: (optional) public key ID
        :param str private_key: (optional) path of private key ID
        :param str region: (optional) region `EU / DE / UK / US / NA / JP`
        :param bool sandbox: (optional) environment SANDBOX(`True`) / LIVE(`False`). Defaults to `False`.
        """
        self.setup(public_key_id, private_key, region, sandbox)

    def setup(self, public_key_id=None, private_key=None, region=None, sandbox=False):
        """
        Setup of the client configuration
        :param str public_key_id: (optional) public key ID
        :param str private_key: (optional) path of private key ID
        :param str region: (optional) region `EU / DE / UK / US / NA / JP`
        :param bool sandbox: (optional) environment SANDBOX(`True`) / LIVE(`False`). Defaults to `False`.
        :return: self
        """
        self.public_key_id = public_key_id
        self.private_key = private_key
        if region is not None:
            self.region = region
            self.__setup_endpoint()
        self.sandbox = sandbox
        return self

    def get_buyer(self, buyer_token):
        """
        Amazon Checkout v2 - Get Buyer
        Get details of Buyer which include buyer ID, name, email address, postal code, and country code
        when used with the Amazon.Pay.renderButton 'SignIn' productType and corresponding signInScopes
        :param str buyer_token: Token used to retrieve buyer details.
            This value is appended as a query parameter to signInReturnUrl.
            Max length: 1000 characters/bytes
        :return: response
        :rtype: requests.Response
        """
        return self.request('GET', f'/buyers/{buyer_token}')

    def create_checkout_session(self, body):
        """
        Amazon Checkout v2 - Create Checkout Session
        Create a new Amazon Pay Checkout Session to customize and manage the buyer experience,
        from when the buyer clicks the Amazon Pay button to when they complete checkout
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/checkout-session.html#request-parameters>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', '/checkoutSessions', body)

    def get_checkout_session(self, checkout_session_id):
        """
        Amazon Checkout v2 - Get Checkout Session
        Get Checkout Session details includes buyer info, payment instrument details, and shipping address.
        Shipping address will only be returned if Checkout Session has PayAndShip product type.
        Use this operation to determine if checkout was successful after the buyer returns
        from the AmazonPayRedirectUrl to the specified checkoutResultReturnUrl
        :param str checkout_session_id: Checkout session identifier
        :return: response
        :rtype: requests.Response
        """
        return self.request('GET', f'/checkoutSessions/{checkout_session_id}')

    def update_checkout_session(self, checkout_session_id, body):
        """
        Amazon Checkout v2 - Update Checkout Session
        Update the Checkout Session with transaction details. You can keep updating the Checkout Session until
        the buyer is redirected to amazonPayRedirectUrl. Once all mandatory parameters have been set,
        the Checkout Session object will respond with a unique amazonPayRedirectUrl that you will use to redirect
        the buyer to complete checkout.
        ChargeAmount to the value that should be processed using the paymentIntent during checkout.
        If you need to split the order to capture additional payment after checkout is complete,
        use the optional totalOrderAmount parameter to set the full order amount
        :param str checkout_session_id: Checkout Session identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/checkout-session.html#request-parameters-2>
        :return: response
        :rtype: requests.Response
        """
        return self.request('PATCH', f'/checkoutSessions/{checkout_session_id}', body)

    def complete_checkout_session(self, checkout_session_id, body):
        """
        Amazon Checkout v2 - Complete Checkout Session
        Complete Checkout Session after the buyer returns to checkoutResultReturnUrl to finalize the paymentIntent.
        The chargeAmount in the request must match the Checkout Session object paymentDetails.chargeAmount to verify
        the transaction amount
        :param str checkout_session_id: Checkout Session identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/checkout-session.html#request-parameters-3>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', f'/checkoutSessions/{checkout_session_id}/complete', body)

    def get_charge_permission(self, charge_permission_id):
        """
        Amazon Checkout v2 - Get Charge Permission
        Get Charge Permission to determine if this Charge Permission can be used to charge the buyer.
        You can also use this operation to retrieve buyer details and their shipping address after a successful checkout.
        You can only retrieve details for 30 days after the time that the Charge Permission was created
        :param str charge_permission_id: Charge Permission identifier
        :return: response
        :rtype: requests.Response
        """
        return self.request('GET', f'/chargePermissions/{charge_permission_id}')

    def update_charge_permission(self, charge_permission_id, body):
        """
        Amazon Checkout v2 - Update Charge Permission
        Update the Charge Permission with your external order metadata or the recurringMetadata if subscription details change
        :param str charge_permission_id: Charge Permission identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/charge-permission.html#request-parameters-1>
        :return: response
        :rtype: requests.Response
        """
        return self.request('PATCH', f'/chargePermissions/{charge_permission_id}', body)

    def close_charge_permission(self, charge_permission_id, body=None):
        """
        Amazon Checkout v2 - Close Charge Permission
        Moves the Charge Permission to a Closed state.
        No future charges can be made and pending charges will be canceled if you set cancelPendingCharges to true
        :param str charge_permission_id: Charge Permission identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/charge-permission.html#request-parameters-2>
        :return: response
        :rtype: requests.Response
        """
        if body is None:
            body = {}

        return self.request('DELETE', f'/chargePermissions/{charge_permission_id}/close', body)

    def create_charge(self, body):
        """
        Amazon Checkout v2 - Create Charge
        Create a Charge to authorize payment if you have a Charge Permission in a Chargeable state.
        You can optionally capture payment immediately by setting captureNow to true.
        You can create up to 25 Charges per one-time Charge Permission
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/charge.html#request-parameters>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', '/charges', body)

    def get_charge(self, charge_id):
        """
        Amazon Checkout v2 - Get Charge
        Get details of Charge such as charge amount and authorization state.
        Use this operation to determine if authorization or capture was successful
        :param str charge_id: Charge identifier
        :return: response
        :rtype: requests.Response
        """
        return self.request('GET', f'/charges/{charge_id}')

    def capture_charge(self, charge_id, body):
        """
        Amazon Checkout v2 - Capture Charge
        Capture payment on a Charge in the Authorized state.
        A successful Capture will move the Charge from Authorized to Captured state.
        The Captured state may be preceded by a temporary CaptureInitiated state
        if payment was captured more than 7 days after authorization.
        An unsuccessful Charge will move to a Declined state if payment was declined
        :param str charge_id: Charge identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/charge.html#request-parameters-2>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', f'/charges/{charge_id}/capture', body)

    def cancel_charge(self, charge_id, body=None):
        """
        Amazon Checkout v2 - Cancel Charge
        Moves Charge to Canceled state and releases any authorized payments.
        You can call this operation until Capture is initiated while Charge is in an AuthorizationInitiated or Authorized state
        :param str charge_id: Charge identifier
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/charge.html#request-parameters-3>
        :return: response
        :rtype: requests.Response
        """
        if body is None:
            body = {}

        return self.request('DELETE', f'/charges/{charge_id}/cancel', body)

    def create_refund(self, body):
        """
        Amazon Checkout v2 - Create Refund
        Initiate a full or partial refund for a Charge.
        At your discretion, you can also choose to overcompensate the buyer and refund more than
        the original Charge amount by either 15% or 75 USD/GBP/EUR or 8,400 YEN (whichever is less)
        :param dict body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/refund.html#request-parameters>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', '/refunds', body)

    def get_refund(self, refund_id):
        """
        Amazon Checkout v2 - Get Refund
        Get details of refund
        :param str refund_id: Refund identifier
        :return: response
        :rtype: requests.Response
        """
        return self.request('GET', f'/refunds/{refund_id}')

    def create_delivery_tracker(self, body):
        """
        Amazon Checkout v2 - Create Delivery Tracker
        Create a Delivery Tracker once an order has been shipped and a tracking code has been generated.
        The buyer will receive a notification on their Alexa-enabled device when the order is shipped and when the order is delivered.
        Note that tracking codes can only be used once
        :param body: request body. See
            <https://developer.amazon.com/docs/amazon-pay-api-v2/delivery-tracker.html#request-parameters>
        :return: response
        :rtype: requests.Response
        """
        return self.request('POST', '/deliveryTrackers', body)

    def request(self, method, api, body=None, query=None):
        """
        Send request to Amazon Pay API.
        The request is signed following steps below.
        - Step 1: Generate a canonical request
            Arrange the contents of your request (host, action, headers, etc.) into a standard (canonical) format.
        - Step 2: Create a String to Sign
            Create a string to sign by concatenating the hashing algorithm designation (AMZN-PAY-RSASSA-PSS) and the digest (hash) of the canonical request.
        - Step 3: Calculate the Signature
            Sign the string to sign using RSASSA-PSS algorithm with SHA256 hashing and then Base64 encode the result.
        - Step 4: Add the Signature to the HTTP Request
            After the signature is calculated, add it as a request header.
        For more information about signing requests, see
            <https://developer.amazon.com/docs/amazon-pay-api-v2/signing-requests.html>
        :param str method: request method. `GET / POST / PATCH / DELETE`
        :param str api: api to call
        :param dict body: request body
        :param dict query: query parameters
        :return: response
        :rtype: requests.Response
        """
        query = query if query is not None else {}
        if type(body) is str:
            payload = body
        elif body is None:
            payload = ''
        else:
            payload = json.dumps(body)

        api = self.__build_api(api)
        headers = self.__build_headers(method, api, query, payload)
        url = self.__build_url(api, query)

        return requests.request(method, url, data=payload, headers=headers)

    def generate_button_signature(self, payload):
        """
        Generate static signature for amazon.Pay.renderButton used by checkout.js
        :param payload: payload that Amazon Pay will use to create a Checkout Session object. See
            <https://developer.amazon.com/docs/amazon-pay-checkout/add-the-amazon-pay-button.html#2-generate-the-create-checkout-session-payload>
        :return: signed signature
        :rtype: str
        """
        if type(payload) is dict:
            payload = json.dumps(payload)

        hashed_button_request = AMAZON_SIGNATURE_ALGORITHM + '\n' + self.__hash_and_hex(payload or '')

        return self.__sign_signature(hashed_button_request)

    def __build_headers(self, method, api, query, payload):
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

        query_string = self.__build_query_string(query)

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Amz-Pay-Region': self.region,
            'X-Amz-Pay-Date': timestamp,
            'X-Amz-Pay-Host': urllib.parse.urlparse(self.endpoint).netloc or '/',
        }

        if method.lower() == 'post':
            headers['X-Amz-Pay-Idempotency-Key'] = uuid.uuid4().hex

        canonical_request = method.upper() + '\n'
        canonical_request += api + '\n'
        canonical_request += query_string + '\n'
        signed_header_list = []
        for header_key in sorted(headers.keys()):
            if headers[header_key] == '' or headers[header_key] is None:
                continue
            canonical_request += header_key.lower() + ':' + headers[header_key] + '\n'
            signed_header_list.append(header_key.lower())
        canonical_request += '\n'
        canonical_request += ';'.join(signed_header_list) + '\n'
        canonical_request += self.__hash_and_hex(payload)

        string_to_sign = AMAZON_SIGNATURE_ALGORITHM + '\n' + self.__hash_and_hex(canonical_request)

        signature = self.__sign_signature(string_to_sign)

        headers['Authorization'] = AMAZON_SIGNATURE_ALGORITHM + \
                                   ' PublicKeyId=' + self.public_key_id + ',' \
                                   ' SignedHeaders=' + ';'.join(signed_header_list) + ',' \
                                   ' Signature=' + signature

        return headers

    @staticmethod
    def __build_query_string(query):
        query_list = []
        for k in sorted(query.keys()):
            if query[k] == '' or query[k] is None:
                continue
            query_name = urllib.parse.quote(k, safe='')
            query_value = urllib.parse.quote(query[k], safe='')
            query_list.append(query_name + '=' + query_value)

        return '&'.join(query_list)

    def __build_url(self, api, query):
        url = self.endpoint + api
        query_string = self.__build_query_string(query)
        if query_string != '':
            url = url + '?' + query_string

        return url

    def __build_api(self, api):
        api = '/v2' + api
        if self.public_key_id.startswith('LIVE') or self.public_key_id.startswith('SANDBOX'):
            return api

        return '/' + ('sandbox' if self.sandbox else 'live') + api

    @staticmethod
    def __hash_and_hex(string):
        return SHA256.new(string.encode()).hexdigest()

    def __sign_signature(self, string_to_sign):
        if self.private_key.find('BEGIN RSA PRIVATE KEY') != -1 and self.private_key.find('BEGIN PRIVATE KEY') != -1:
            private = self.private_key
        else:
            private_key = open(self.private_key, 'r')
            private = private_key.read()
            private_key.close()

        rsa = RSA.import_key(private)
        signature = pss.new(rsa, salt_bytes=20).sign(SHA256.new(string_to_sign.encode()))
        return base64.b64encode(signature).decode()

    def __setup_endpoint(self):
        region_mappings = {
            'eu': 'eu',
            'de': 'eu',
            'uk': 'eu',
            'us': 'na',
            'na': 'na',
            'jp': 'jp'
        }

        endpoint_mappings = {
            'eu': 'pay-api.amazon.eu',
            'na': 'pay-api.amazon.com',
            'jp': 'pay-api.amazon.jp'
        }

        region = self.region.lower()
        if region not in region_mappings:
            raise Exception(self.region + ' is not a valid region.')

        self.endpoint = 'https://' + endpoint_mappings[region]
        return self
