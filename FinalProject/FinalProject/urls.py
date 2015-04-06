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
    url(r'^socialnetwork/edit$', 'socialnetwork.views.edit', name='edit'),
    url(r'^socialnetwork/profile/(?P<id>\d+)$', 'socialnetwork.views.profile', name='profile'),
    url(r'^socialnetwork/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^socialnetwork/add_class$', 'socialnetwork.views.add_class', name='add_class'),
    url(r'^socialnetwork/add_post/(?P<name>\d\d\d\d\d)$', 'socialnetwork.views.add_post', name='add_post'),
    url(r'^socialnetwork/show_post/(?P<id>\d+)$', 'socialnetwork.views.show_post', name='show_post'),
    url(r'^socialnetwork/add_comment/(?P<id>\d+)$', 'socialnetwork.views.add_comment', name='add_comment'),
    url(r'^socialnetwork/change_class/(?P<name>\d\d\d\d\d+)$', 'socialnetwork.views.change_class', name='change_class'),
    # url(r'^socialnetwork/edit/$', 'socialnetwork.views.edit', name='edit'),
    # url(r'^socialnetwork/profile/(?P<user>\w+)$', 'socialnetwork.views.profile', name='profile'),
)
