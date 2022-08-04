try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.profile.views as profile

urlpatterns = [
    # profile change_password/top
    _url(r'^$', profile.change_password_top),
    # profile change_password
    _url(r'^change_password$', profile.change_password, name='password_modified'),
    # profile change_screen_name
    _url(r'^change_screen_name$', profile.change_screen_name),
]
