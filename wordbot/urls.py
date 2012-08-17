from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('wordbot.views',
    # Examples:
    url(r'^$', 'home'),
    url(r'^get_token/$', 'get_token'),
    url(r'^oauth_callback/$', 'oauth_callback'),
    url(r'^callback/$', 'callback'),
                       
    url(r'^test/$', 'test'),
    url(r'^bot_create/$', 'bot_create'),
    url(r'^bot_update/$', 'bot_update'),
    url(r'^callback/$', 'callback'),

    url(r'^add_survey/$', 'add_survey'),
    url(r'^add_question/$', 'add_question'),
    url(r'^add_answer/$', 'add_answer'),
    url(r'^add_result/$', 'add_result'),
    url(r'^add_basic_answer/$', 'add_basic_answer'),

    url(r'^remove_question/$', 'remove_question'),
    url(r'^remove_answer/$', 'remove_answer'),
    url(r'^remove_survey/$', 'remove_survey'),
    url(r'^remove_result/$', 'remove_result'),
                       
    # url(r'^mypeoplebot/', include('mypeoplebot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
