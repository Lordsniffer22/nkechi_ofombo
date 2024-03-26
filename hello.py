import requests

# Replace with your Flutterwave API keys
FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK_TEST-1b2607d27bedc182f378e2f7d763f9ae-X'
FLUTTERWAVE_SECRET_KEY = 'FLWSECK_TEST-a589b84f8c701ed15fa08014d7c778ff-X'

# Endpoint for initiating payment
payment_url = 'https://api.flutterwave.com/v3/payments'

# Sample payload for initiating payment
payload = {
    "tx_ref": "test_transaction",
    "amount": "100",
    "currency": "USD",
    "redirect_url": "https://t.me/hackwell101",
    "payment_options": "card",
    "meta": {
        "consumer_id": 23,
        "consumer_mac": "92a3-912ba-1192a"
    },
    "customer": {
        "email": "user@example.com",
        "phone_number": "08102909304",
        "name": "Test User"
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
    payment_link = payment_data['data']['link']
    print("Payment link:", payment_link)
else:
    print("Failed to initiate payment:", response.text)
