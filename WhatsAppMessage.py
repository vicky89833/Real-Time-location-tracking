import requests

app_id = "691910346662512"
app_secret = "82876125524cf8fa95698418feeeb6f0"
phone_number_id = "YOUR_PHONE_NUMBER_ID"
recipient_number = "RECIPIENT_NUMBER"  # with country code, no + or 00
access_token = "YOUR_ACCESS_TOKEN"

url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": recipient_number,
    "type": "text",
    "text": {
        "body": "Hello from WhatsApp API!"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
