#!/usr/bin/env python
# coding: utf-8

# Django imports
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings


def send_text_email(subject, body, email_to, bcc=[]):
    """
    Send text emails
    :param title:
    :param body:
    :param email_from:
    :param email_to:
    :return:
    """
    email = EmailMessage(
        subject=subject,
        body=body,
        to=email_to,
        bcc=bcc
    )
    return email.send()


def send_mail_from_html(subject, body, email_to, bcc=[]):

    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        to=email_to,
        bcc=bcc
    )
    email.attach_alternative(body, 'text/html')
    return email.send()