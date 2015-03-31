from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FinalProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'socialnetwork.views.home', name='home'),
    url(r'^socialnetwork/login$', 'django.contrib.auth.views.login', {'template_name':'socialnetwork/login.html'}, name='login'),
    url(r'^socialnetwork/register$', 'socialnetwork.views.register', name='register'),
    url(r'^socialnetwork/map$', 'socialnetwork.views.map', name='map'),
    url(r'^socialnetwork/edit/$', 'socialnetwork.views.edit', name='edit'),
    url(r'^socialnetwork/profile/(?P<id>\d+)$', 'socialnetwork.views.profile', name='profile'),
    url(r'^socialnetwork/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^socialnetwork/add_class/(?P<user>\w+)$', 'socialnetwork.views.add_class', name='add_class'),
    # url(r'^socialnetwork/edit/$', 'socialnetwork.views.edit', name='edit'),
    # url(r'^socialnetwork/profile/(?P<user>\w+)$', 'socialnetwork.views.profile', name='profile'),
)
