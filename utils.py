# from twilio.rest import Client

# # Twilio credentials (commented out for now)
# ACCOUNT_SID = 'your_account_sid'
# AUTH_TOKEN = 'your_auth_token'
# TWILIO_PHONE_NUMBER = '+1234567890'

# client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms_alert(patient):
    # Dummy alert function - for now just print message to console
    message = f"Dummy Alert: {patient.name} needs urgent attention!"
    print(message)

    # Uncomment below code and fill real credentials when ready to send SMS via Twilio

    # try:
    #     message = client.messages.create(
    #         body=message,
    #         from_=TWILIO_PHONE_NUMBER,
    #         to='+918xxxxxxxxx'  # Caregiver’s phone number
    #     )
    #     print('Alert sent:', message.sid)
    # except Exception as e:
    #     print('Failed to send alert:', e)
