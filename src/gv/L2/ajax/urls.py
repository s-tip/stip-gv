try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.L2.ajax.views as ajax

urlpatterns = [
    # related_packages
    _url(r'^related_packages$', ajax.related_packages),
    # related_package_nodes
    _url(r'^related_package_nodes$', ajax.related_package_nodes),
    # create_opinion
    _url(r'^create_opinion$', ajax.create_opinion),
    # create_note
    _url(r'^create_note$', ajax.create_note),
    # revoke
    _url(r'^revoke$', ajax.revoke),
    # modify
    _url(r'^modify$', ajax.modify),
    # get_stix2_content
    _url(r'^get_stix2_content$', ajax.get_stix2_content),
]
