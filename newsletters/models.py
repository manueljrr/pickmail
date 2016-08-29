#!/usr/bin/env python
# coding: utf-8

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Local imports
from .constants import EMAIL_TYPE_TEXT, EMAIL_TYPE_CHOICES


class ContactList(models.Model):
    """
    List or group of contacts to send a newsletter
    """
    created = models.DateTimeField(
        verbose_name=_(u'Created at'),
        auto_now_add=True
    )
    list_name = models.CharField(
        verbose_name=_(u'List name'),
        unique=True,
        max_length=100
    )

    def __str__(self):
        return self.list_name


class Contact(models.Model):
    """
    Data of mail contacts to send newsletters
    """
    created = models.DateTimeField(
        verbose_name=_(u'Created at'),
        auto_now_add=True
    )
    last_update = models.DateTimeField(
        verbose_name=_(u'Last update'),
        auto_now=True
    )
    name = models.CharField(
        verbose_name=_(u'Name'),
        max_length=100,
        null=True,
        blank=True
    )
    surname = models.CharField(
        verbose_name=_(u'Surname'),
        max_length=100,
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name=_(u'Email'),
        unique=True,
        max_length=100
    )
    contact_lists = models.ManyToManyField(
        ContactList,
        related_name='contacts',
        blank=True
    )

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    """
    Newsletter (email) information and settings for sending mails
    """
    created = models.DateTimeField(
        verbose_name=_(u'Created at'),
        auto_now_add=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_(u'Created by'),
        limit_choices_to={'is_staff': True}
    )
    subject = models.CharField(
        verbose_name=_(u'Email Subject'),
        max_length=200
    )
    content_type = models.IntegerField(
        verbose_name=_(u'Content type'),
        choices=EMAIL_TYPE_CHOICES,
        default=EMAIL_TYPE_TEXT
    )
    content = models.TextField(
        verbose_name=_(u'Content'),
        null=True,
        blank=True
    )
    url = models.URLField(
        verbose_name=_(u'URL content'),
        null=True,
        blank=True
    )
    email_from = models.EmailField(
        verbose_name=_(u'From'),
        max_length=100
    )
    send_to = models.ForeignKey(
        ContactList,
        verbose_name=_(u'List to send email')
    )
    bcc = models.ManyToManyField(
        User,
        verbose_name=_(u'BCC'),
        related_name='bcc_in_news',
        help_text=_(u'Staff users who will receive BCC email'),
        blank=True
    )

    def __str__(self):
        return self.subject

    def get_email_contact_list(self):
        email_list = [contact.email for contact in self.send_to.contacts.all()]
        return email_list

    def get_bcc_email_list(self):
        email_list = [bcc.email for bcc in self.bcc.all()]
        return email_list

