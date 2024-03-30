#!/bin/bash

# Replace 'YOUR_FLUTTERWAVE_API_KEY' with your actual Flutterwave API key
FLUTTERWAVE_API_KEY="FLWPUBK-0e4658e40b88a018d1451da348f9acab-X"

# Default customer details
CUSTOMER_EMAIL="owori@gmail.com"

# Function to generate payment link
generate_payment_link() {
    local amount="$1"
    local response=$(curl -s -X POST "https://api.flutterwave.com/v3/payments" \
        -H "Authorization: Bearer $FLUTTERWAVE_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"amount\":$amount,\"currency\":\"UGX\",\"tx_ref\":\"your_transaction_reference\",\"redirect_url\":\"your_redirect_url\",\"payment_options\":\"mobilemoneyuganda\",\"customer\":{\"email\":\"$CUSTOMER_EMAIL\"}}")

    local payment_link=$(echo "$response" | jq -r '.data.link')
    if [ -n "$payment_link" ]; then
        echo "Payment link: $payment_link"
    else
        echo "Failed to generate payment link."
    fi
}

# Main
if [ $# -eq 0 ]; then
    echo "Usage: $0 <amount>"
    exit 1
fi

amount=$1
generate_payment_link "$amount"
