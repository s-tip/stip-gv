from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.L2.views as l2
import gv.L2.ajax.urls

urlpatterns = [
    # L2 view/top
    _url(r'^$', l2.l2_view_top),
    # L2 ajax
    _url(r'^ajax/', include(gv.L2.ajax.urls)),
]
