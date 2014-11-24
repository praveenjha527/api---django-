from django.conf.urls import patterns, include, url
from login.views import * #fetchdata, createevent
from notifications.views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', data),
    #url(r'^populatedb/$', csrf_exempt(PopulateDatabase.as_view())),
    url(r'^profile/$', profile),
    url(r'^updatelocation/$', updatelocation),
    url(r'^addslot/$', addslot),
    url(r'^removeslot/$', removeslot),
    url(r'^match/$', match),
    url(r'^invite/$', invite),
    url(r'^response/$', response),
    url(r'^getinvites/$', getinvites),
    url(r'^cancelinvite/$', cancelinvite),
    url(r'^addfav/$', addfav),
    url(r'^addblock/$', addblock),
    url(r'^notifications/$', notifications_register),
    url(r'^getslots/$', getslots),
)