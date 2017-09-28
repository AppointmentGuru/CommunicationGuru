# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CommunicationTemplate, Communication, CommunicationStatus

class CommunicationStatusInline(admin.TabularInline):
    model = CommunicationStatus

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('preferred_transport', 'backend_used', 'backend_message_id', 'sender_email', 'recipient_emails', 'recipient_phone_number', 'subject', 'send_date')
    list_filter = ('owner', 'object_ids', 'sender_email', 'backend_message_id', 'backend_used')
    inlines = [CommunicationStatusInline]

class CommunicationStatusAdmin(admin.ModelAdmin):
    list_display = ('communication', 'status', 'created_date')

admin.site.register(Communication, CommunicationAdmin)
admin.site.register(CommunicationStatus, CommunicationStatusAdmin)
admin.site.register(CommunicationTemplate)
