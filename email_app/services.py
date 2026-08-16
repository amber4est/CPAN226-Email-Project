from django.core.mail import EmailMessage

# send email message
def send_email_message(
    sender,
    receiver,
    subject,
    message,
    cc_recipients = None,
    attachment = None,
):
    # email information
    email = EmailMessage(
        subject = subject,
        body = message,
        from_email = sender,
        to = [receiver],
        cc = cc_recipients or [],
    )

    # check for attachment
    if attachment:
        email.attach(
            attachment.name,
            attachment.read(),
            attachment.content_type,
        )

    # send email
    email.send()