from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from catalog.views import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',main_page),
    url(r'^catalog/(\d+)/$', 'catalog.views.catalog'),
    url(r'^details/([-\w]+)/$', 'catalog.views.details'),
    (r'^ajax/$', ajax),
    (r'^search/$', search),
    (r'^order/$', order),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^tinymce/', include('tinymce.urls')), what's the reason?
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )