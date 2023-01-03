import os
import unittest
import yaml
from AmazonPay import Client


class AmazonPayClientTest(unittest.TestCase):

    def test_get_buyer(self):
        buyer_token = self.config['buyer_token']

        response = self.client.get_buyer(buyer_token)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

    def test_create_checkout_session(self):
        body = {
            'webCheckoutDetails': {
                'checkoutReviewReturnUrl': 'https://localhost/store/checkout_review',
                'checkoutResultReturnUrl': 'https://localhost/store/checkout_result'
            },
            'chargePermissionType': 'OneTime',
            'paymentDetails': {
                'paymentIntent': 'AuthorizeWithCapture',
                'chargeAmount': {
                    'amount': '100',
                    'currencyCode': 'JPY'
                }
            },
            'storeId': self.config['store_id']
        }

        response = self.client.create_checkout_session(body)

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

    def test_get_checkout_session(self):
        checkout_session_id = self.config['confirmed_checkout_session_id']

        response = self.client.get_checkout_session(checkout_session_id)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['checkoutSessionId'], checkout_session_id, f"Invalid checkout-session-id. Except [{checkout_session_id}], got [{result['checkoutSessionId']}]")

    def test_update_checkout_session(self):
        response = self.client.create_checkout_session({
            'webCheckoutDetails': {
                'checkoutReviewReturnUrl': 'https://localhost/store/checkout_review',
                'checkoutResultReturnUrl': 'https://localhost/store/checkout_result'
            },
            'chargePermissionType': 'OneTime',
            'paymentDetails': {
                'paymentIntent': 'AuthorizeWithCapture',
                'chargeAmount': {
                    'amount': '100',
                    'currencyCode': 'JPY'
                }
            }
        })

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

        checkout_session_id = response.json()['checkoutSessionId']
        update_charge_amount_to = '50'
        body = {
            'paymentDetails': {
                'chargeAmount': {
                    'amount': update_charge_amount_to,
                    'currencyCode': 'JPY'
                }
            }
        }

        response = self.client.update_checkout_session(checkout_session_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['paymentDetails']['chargeAmount']['amount'], update_charge_amount_to, f"Invalid charge amount. Except {update_charge_amount_to}, got [{result['paymentDetails']['chargeAmount']['amount']}]")

    def test_complete_checkout_session(self):
        checkout_session_id = self.config['confirmed_checkout_session_id']

        response = self.client.get_checkout_session(checkout_session_id)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        body = {
            'chargeAmount': response.json()['paymentDetails']['chargeAmount']
        }

        response = self.client.complete_checkout_session(checkout_session_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['statusDetails']['state'], 'Completed', f"Invalid state. Except [Completed], got [{result['statusDetails']['state']}]")

    def test_get_charge_permission(self):
        charge_permission_id = self.config['chargeable_charge_permission_id']

        response = self.client.get_charge_permission(charge_permission_id)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['chargePermissionId'], charge_permission_id, f"Invalid charge-permission-id. Except [{charge_permission_id}], got [{result['chargePermissionId']}]")

    def test_update_charge_permission(self):
        charge_permission_id = self.config['chargeable_charge_permission_id']
        test_merchant_metadata = '00-00-000000-00'
        body = {
            'merchantMetadata': {
                'merchantReferenceId': test_merchant_metadata,
                'merchantStoreName': 'Test Store',
                'noteToBuyer': 'Some Note to buyer',
                'customInformation': 'Custom Information'
            }
        }

        response = self.client.update_charge_permission(charge_permission_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['merchantMetadata']['merchantReferenceId'], test_merchant_metadata, f"Invalid merchant-metadata. Except [{test_merchant_metadata}], got [{result['merchantMetadata']['merchantReferenceId']}]")

    def test_close_charge_permission(self):
        charge_permission_id = self.config['chargeable_charge_permission_id']
        body = {
            'closureReason': 'No more charges required',
            'cancelPendingCharges': False
        }

        response = self.client.close_charge_permission(charge_permission_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['statusDetails']['state'], 'Closed', f"Invalid state. Except [Closed], got [{result['statusDetails']['state']}]")

    def test_create_charge(self):
        body = {
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'chargeAmount': {
                'amount': '1',
                'currencyCode': 'JPY'
            },
            'captureNow': True
        }

        response = self.client.create_charge(body)

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

    def test_get_charge(self):
        response = self.client.create_charge({
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'chargeAmount': {
                'amount': '1',
                'currencyCode': 'JPY'
            },
            'captureNow': True
        })

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

        charge_id = response.json()['chargeId']

        response = self.client.get_charge(charge_id)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['chargeId'], charge_id, f"Invalid charge-permission-id. Except [{charge_id}], got [{result['chargeId']}]")

    def test_capture_charge(self):
        response = self.client.create_charge({
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'chargeAmount': {
                'amount': '5',
                'currencyCode': 'JPY'
            },
            'captureNow': False
        })

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

        charge_id = response.json()['chargeId']
        body = {
            'captureAmount': {
                'amount': '1',
                'currencyCode': 'JPY'
            }
        }

        response = self.client.capture_charge(charge_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['statusDetails']['state'], 'Captured', f"Invalid charge-permission-id. Except [Captured], got [{result['statusDetails']['state']}]")

    def test_cancel_charge(self):
        response = self.client.create_charge({
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'chargeAmount': {
                'amount': '1',
                'currencyCode': 'JPY'
            },
            'captureNow': False
        })

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

        charge_id = response.json()['chargeId']
        body = {
            'cancellationReason': 'REASON DESCRIPTION'
        }

        response = self.client.cancel_charge(charge_id, body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['statusDetails']['state'], 'Canceled', f"Invalid charge-permission-id. Except [Canceled], got [{result['statusDetails']['state']}]")

    def test_create_refund(self):
        response = self.client.create_charge({
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'chargeAmount': {
                'amount': '5',
                'currencyCode': 'JPY'
            },
            'captureNow': True
        })

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

        body = {
            'chargeId': response.json()['chargeId'],
            'refundAmount': {
                'amount': '1',
                'currencyCode': 'JPY'
            },
        }

        response = self.client.create_refund(body)

        self.assertEqual(response.status_code, 201, response.content.decode(encoding='utf-8'))

    def test_get_refund(self):
        refund_id = self.config['refund_id']

        response = self.client.get_refund(refund_id)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

        result = response.json()

        self.assertEqual(result['refundId'], refund_id, f"Invalid charge-permission-id. Except [{refund_id}], got [{result['refundId']}]")

    def test_create_delivery_tracker(self):
        body = {
            'chargePermissionId': self.config['chargeable_charge_permission_id'],
            'deliveryDetails': [
                {
                    'carrierCode': self.config['carrier_code'],
                    'trackingNumber': self.config['tracking_number']
                }
            ]
        }

        response = self.client.create_delivery_tracker(body)

        self.assertEqual(response.status_code, 200, response.content.decode(encoding='utf-8'))

    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), encoding='utf-8') as config_file:
            self.config = yaml.safe_load(config_file)

        config = {
            'public_key_id': self.config['public_key_id'],
            'private_key': os.path.join(os.path.dirname(__file__), self.config['private_key']),
            'region': self.config['region']
        }

        self.client = Client(**config)

    def tearDown(self):
        pass
