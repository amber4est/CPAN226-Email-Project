from django.urls import path
from . import views

urlpatterns = [
    path("", views.test_email_form, name="test_email_form"),
    path("send-email/", views.send_email, name="send_email"),
]