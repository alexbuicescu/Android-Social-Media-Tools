from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from fb.views import (
    add_user, show_users,
    index, post_details, login_view, logout_view, profile_view,
    edit_profile_view, like_view,
)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^users/$', show_users, name='show_users'),
    url(r'^adduser/$', add_user, name='add_user'),
    url(r'^post/(?P<pk>\d)/$', post_details, name='post_details'),
    url(r'^post/(?P<pk>\d)/like$', like_view, name='like'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<user>\w+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<user>\w+)/edit$', edit_profile_view,
        name='edit_profile'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
