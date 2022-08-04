from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.dashboard.views as dashboard
import gv.dashboard.ajax.urls

urlpatterns = [
    # dashboard view/top
    _url(r'^$', dashboard.dashboard_view_top, name='dashboard'),
    # dashboard ajax
    _url(r'^ajax/', include(gv.dashboard.ajax.urls)),
]
