"""communications URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^incoming/slack/$', api.slack_webhook, name='slack_webhook'),
    url(r'^messages/backends/(?P<transport>[\w-]+)/$',
        api.backends_messages, name='backend_messages'),
    url(r'^incoming/(?P<token>[\w-]+)/(?P<transport>[\w-]+)/(?P<update_type>[\w-]+)/(?P<backend>[\w-]+)/$',
        api.incoming,
        name='incoming_update'),
    url(r'^$', api.health, name='health'),
    url(r'^', include(api.router.urls)),
]
