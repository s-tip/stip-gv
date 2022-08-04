try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.configuration.alias.views as alias

urlpatterns = [
    _url(r'^$', alias.alias_view_top),
    _url(r'^create_alias$', alias.create_alias),
    _url(r'^delete_alias$', alias.delete_alias),
]
