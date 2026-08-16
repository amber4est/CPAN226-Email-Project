from django.core.mail import EmailMessage

def send_email_message(
    sender,
    receiver,
    subject,
    message,
    cc_recipients = None,
    attachment = None,
):
    email = EmailMessage(
        subject = subject,
        body = message,
        from_email = sender,
        to = [receiver],
        cc = cc_recipients or [],
    )

    if attachment:
        email.attach(
            attachment.name,
            attachment.read(),
            attachment.content_type,
        )

    email.send()