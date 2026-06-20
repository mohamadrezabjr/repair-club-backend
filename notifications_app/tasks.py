from notifications_app.factory.mapping import FACTORY_MAPPING

def send_notification(event, recipient_info, context):
    factory = FACTORY_MAPPING.get(event)
    if not factory:
        raise ValueError('Unknown event: {}'.format(event))

    notification = factory().create_notification(context)
    notification.send(recipient_info)