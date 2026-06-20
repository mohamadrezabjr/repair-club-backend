from notifications_app.providers.base import BaseSMSProvider

class TestSMSProvider(BaseSMSProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def send_sms(self, phone, message):
        print(f'Sending SMS: {message} to {phone} with key: {self.api_key}')