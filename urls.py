from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'testdj.backend.login.login', name='index'),
    url(r'^login/?$', 'testdj.backend.login.login', name='login'),
    url(r'^welcome/?$', 'testdj.backend.login.welcome', name='welcome'),
    url(r'^wel/?$', 'testdj.backend.login.wel', name='wel'),
    url(r'^logout/?$', 'testdj.backend.login.logout', name='logout'),
    # url(r'^testdj/', include('testdj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
