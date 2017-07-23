# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CommunicationTemplate, Communication

admin.site.register(Communication)
admin.site.register(CommunicationTemplate)
