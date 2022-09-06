from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.sharing.views as sharing
import gv.sharing.ajax.urls

urlpatterns = [
    # Sharing view/top
    _url(r'^$', sharing.sharing_view_top),
    # stix_upload更新
    _url(r'^stix_upload$', sharing.stix_upload),
    # download
    _url(r'^stix_download$', sharing.stix_download),
    # csv-download
    _url(r'^stix_data_csv_download$', sharing.stix_data_csv_download),
    # delete package
    _url(r'^delete_package$', sharing.delete_package),
    # sharing ajax
    _url(r'^ajax/', include(gv.sharing.ajax.urls)),
]
