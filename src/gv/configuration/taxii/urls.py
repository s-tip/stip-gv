try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.configuration.taxii.views as taxii

urlpatterns = [
    # configuration/taxii view/top
    _url(r'^$', taxii.taxii_view_top),
    # configuration/taxii create_taxii
    _url(r'^create_taxii$', taxii.create_taxii),
    # configuration/taxii delete_taxii
    _url(r'^delete_taxii$', taxii.delete_taxii),
]
