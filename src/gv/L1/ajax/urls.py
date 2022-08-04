try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.L1.ajax.views as ajax

urlpatterns = [
    _url(r'^get_l1_info_data_tables', ajax.get_l1_info_data_tables),
    _url(r'^create_sighting', ajax.create_sighting),
]
