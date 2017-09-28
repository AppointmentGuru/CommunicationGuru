# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CommunicationTemplate, Communication, CommunicationStatus

admin.site.register(Communication)
admin.site.register(CommunicationStatus)
admin.site.register(CommunicationTemplate)
