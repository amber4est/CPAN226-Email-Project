from django.http import JsonResponse
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .services import send_email_message
from django.core.mail import BadHeaderError

# sending an email
def send_email(request):
    # check if POST or not
    if request.method != "POST":
        # error message
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    # proceed with sending email

    # get email information
    sender = request.POST.get("sender", "").strip()
    receiver = request.POST.get("receiver", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    cc = request.POST.get("cc", "").strip()

    # check required fields
    if not sender or not receiver or not subject or not message:
        return JsonResponse(
            {
                "error": (
                    "Sender, receiver, subject, and message are required."
                )
            },
            status=400
        )

    # validate sender email
    try:
        validate_email(sender)
    except ValidationError:
        return JsonResponse(
            {"error": "Invalid sender email address."},
            status=400
        )

    # validate receiver email
    try:
        validate_email(receiver)
    except ValidationError:
        return JsonResponse(
            {"error": "Invalid receiver email address."},
            status=400
        )

    # seperate CC recipients
    cc_recipients = []

    if cc:
        cc_recipients = [
            email.strip()
            for email in cc.split(",")
            if email.strip()
        ]

        # validate every CC address
        for email in cc_recipients:
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse(
                    {"error": f"Invalid CC email address: {email}"},
                    status=400
                )

    # send email
    try:
        send_email_message(
            sender=sender,
            receiver=receiver,
            subject=subject,
            message=message,
            cc_recipients=cc_recipients,
            attachment=request.FILES.get("attachment"),
        )

        # success message
        return JsonResponse(
            {"message": "Email sent successfully."}
        )

    # error message
    except BadHeaderError:
        return JsonResponse(
            {"error": "Invalid email header."},
            status=400
        )
    # exception/error message
    except Exception:
        return JsonResponse(
            {"error": "Failed to send email. Please try again."},
            status=500
        )

# test email form
def test_email_form(request):
    return render(request, "email_app/test_email.html")