from notifications_app.factory.base import BaseNotification, BaseNotificationFactory
from config.settings import get_active_sms_provider

class VisitCheckInSMS(BaseNotification):
    def __init__(self, context):
        self.context = context
        self.message = None

    def prepare_content(self, context= None):
        ctx = context or self.context
        services = ctx.get('services', [])

        customer_name = ctx.get('name', 'مشتری گرامی')
        plate_number = ctx.get('plate_number', '---')

        base_text = (
            f"مشترک گرامی {customer_name}، خودروی "
            f"شما با پلاک {plate_number} در اتوسرویس پذیرش شد.\n"
            f"خدمات درخواستی:\n"
        )

        services_list_text = "".join(
            f"{index}. {service}\n" for index, service in enumerate(services, start=1)
        )

        self.message = base_text + services_list_text + "از اعتماد شما سپاسگزاریم."
        return self.message

    def send(self, recipient_info):

        if not self.message:
            self.prepare_content()

        phone = recipient_info.get('phone')
        if not phone:
            raise ValueError("phone number is required")
        sms_provider = get_active_sms_provider()
        sms_provider.send(phone, self.message)

class VisitCheckInSMSFactory(BaseNotificationFactory):
    def create_notification(self, context=None, **kwargs):
        return VisitCheckInSMS(context)