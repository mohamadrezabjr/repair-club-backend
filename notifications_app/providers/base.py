from abc import ABC, abstractmethod

class BaseSMSProvider(ABC):
    @abstractmethod
    def send_sms(self, phone, message):
        pass

class BaseEmailProvider(ABC):
    @abstractmethod
    def send_email(self, to, subject, message):
        pass