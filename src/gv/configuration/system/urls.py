try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.configuration.system.views as system

urlpatterns = [
    # configuration/system top
    _url(r'^$', system.system_view_top),
    # configuration/system modify
    _url(r'^modify$', system.system_modify),
]
