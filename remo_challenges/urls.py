from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'remo_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^event-metrics', 'dashboard.views.event_metrics', name='event-metrics'),
    url(r'^$', 'dashboard.views.home', name='home'),
)
