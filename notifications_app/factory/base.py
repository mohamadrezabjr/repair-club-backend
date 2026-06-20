from abc import ABC, abstractmethod

class BaseNotificationFactory(ABC):
    @abstractmethod
    def create_notification(self, context, **kwargs):
        pass

class BaseNotification(ABC):
    @abstractmethod
    def prepare_content(self, context):
        pass
    @abstractmethod
    def send(self, recipient):
        pass