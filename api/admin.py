# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    CommunicationTemplate,
    Communication,
    CommunicationStatus,
    IncomingInformation
)

class CommunicationStatusInline(admin.TabularInline):
    model = CommunicationStatus

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'backend_used', 'backend_message_id', 'sender_email', 'recipient_emails', 'recipient_phone_number', 'channel', 'subject', 'send_date')
    list_filter = ('owner', 'backend_used')
    list_search = ('object_ids', 'sender_email', 'recipient_emails', 'recipient_phone_number', 'channel', 'backend_message_id',)
    inlines = [CommunicationStatusInline]

class CommunicationStatusAdmin(admin.ModelAdmin):
    list_display = ('communication', 'status', 'created_date',)
    list_filter = ('status',)

class IncomingInformationAdmin(admin.ModelAdmin):
    list_display = ('backend', 'type',)
    list_filter = ('backend', 'type',)

class CommunicationTemplateAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'slug',)
    list_filter = ('owner', 'slug',)


admin.site.register(Communication, CommunicationAdmin)
admin.site.register(CommunicationStatus, CommunicationStatusAdmin)
admin.site.register(CommunicationTemplate, CommunicationTemplateAdmin)
admin.site.register(IncomingInformation, IncomingInformationAdmin)