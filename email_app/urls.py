from django.urls import path
from . import views

urlpatterns = [
    # test email form
    path("", views.test_email_form, name="test_email_form"),
    # send email form
    path("send-email/", views.send_email, name="send_email"),
]