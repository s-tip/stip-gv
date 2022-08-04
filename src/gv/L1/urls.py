from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.L1.views as l1
import gv.L1.ajax.urls

urlpatterns = [
    # L1 view/top
    _url(r'^$', l1.l1_view_top),
    # L1 view/download_stix
    _url(r'^download_stix', l1.download_stix),
    # L1 ajax
    _url(r'^ajax/', include(gv.L1.ajax.urls)),
]
