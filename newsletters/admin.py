#!/usr/bin/env python
# coding: utf-8

# Python imports
import urllib2
from ckeditor.widgets import CKEditorWidget

# Django imports
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import pluralize
from django.db import models

# Local imports
from .models import *
from .constants import EMAIL_TYPE_TEXT, EMAIL_TYPE_URL, EMAIL_TYPE_HTML
from .mail import send_text_email, send_mail_from_html


@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    filter_horizontal = ['contact_lists']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    filter_horizontal = ['bcc']

    actions = ['admin_send_newsletter']

    def admin_send_newsletter(self, request, queryset):
        sends = 0
        fails = queryset.all().count()
        contacts = 0
        for newsletter in queryset.all():
            if newsletter.content_type == EMAIL_TYPE_TEXT:
                result = send_text_email(
                    subject=newsletter.subject,
                    body=newsletter.content,
                    email_to=newsletter.get_email_contact_list(),
                    bcc=newsletter.get_bcc_email_list()
                )
            elif newsletter.content_type == EMAIL_TYPE_HTML:
                result = send_mail_from_html(
                    subject=newsletter.subject,
                    body=newsletter.content,
                    email_to=newsletter.get_email_contact_list(),
                    bcc=newsletter.get_bcc_email_list()
                )
            elif newsletter.content_type == EMAIL_TYPE_URL:
                html_content = urllib2.urlopen(newsletter.url).read()
                result = send_mail_from_html(
                    subject=newsletter.subject,
                    body=html_content,
                    email_to=newsletter.get_email_contact_list(),
                    bcc=newsletter.get_bcc_email_list()
                )

            sends += result
            if result:
                contacts += len(newsletter.get_email_contact_list())

        # Set response message and finish
        fails -= sends
        response_msg = _(u'%d newsletter%s sent to %d contact%s, %d failed' %
                         (sends, pluralize(sends), contacts, pluralize(contacts), fails))
        self.message_user(request, response_msg)

    admin_send_newsletter.short_description = _(u'Send selected newsletter')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

