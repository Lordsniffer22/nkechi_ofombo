import requests

# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-0e4658e40b88a018d1451da348f9acab-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK-2cfcb60ea041cb576453e651c9ee2e43-18e7acefd71vt-X'

# Endpoint for initiating payment
payment_url = 'https://api.flutterwave.com/v3/payments'

# Sample payload for initiating payment
payload = {
    "tx_ref": "test_transaction",
    "amount": "100",
    "currency": "UGX",
    "payment_options": "mobilemoneyuganda",
    "redirect_url": "https://your-redirect-url.com",
    "meta": {
        "consumer_id": 23,
        "consumer_mac": "92a3-912ba-1192a"
    },
    "customer": {
        "email": "user@example.com",
        "phone_number": "256742067406",  # Replace with your phone number
        "name": "OWORI NICHOLOUS"
    },
    "customizations": {
        "title": "Test Payment",
        "description": "Payment for test purposes"
    }
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
}

# Initiate payment
response = requests.post(payment_url, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    payment_data = response.json()
    payment_details = payment_data['data']
    print("Payment details:", payment_details)
else:
    print("Failed to initiate payment:", response.text)
