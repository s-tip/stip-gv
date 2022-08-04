try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.sharing.ajax.views as ajax

urlpatterns = [
    # getrawstix
    _url(r'^getrawstix$', ajax.get_raw_stix),
    # getdrawdata
    _url(r'^getdrawdata$', ajax.get_draw_data),
    # send_taxi
    _url(r'^send_taxii', ajax.send_taxii),
    # get_upload_stix
    _url(r'^get_upload_stix', ajax.get_upload_stix),
    # change_stix_comment
    _url(r'^change_stix_comment$', ajax.change_stix_comment),
    # get_stix_comment
    _url(r'^get_stix_comment$', ajax.get_stix_comment),
    # get_package_table
    _url(r'^get_package_table', ajax.get_package_table),
    # create_language_content
    _url(r'^create_language_content', ajax.create_language_content),
]
