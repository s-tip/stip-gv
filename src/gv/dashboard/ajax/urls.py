try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.dashboard.ajax.views as ajax

urlpatterns = [
    # get_stix_counts
    _url(r'^get_stix_counts$', ajax.get_stix_counts),
    # get_pacakge_info
    _url(r'^get_package_info', ajax.get_package_info),
]
