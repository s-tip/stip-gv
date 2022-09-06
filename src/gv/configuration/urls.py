from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.configuration.taxii.urls
import gv.configuration.system.urls
import gv.configuration.alias.urls

urlpatterns = [
    # configuration/taxii
    _url(r'^taxii/', include(gv.configuration.taxii.urls)),
    # configuration/system
    _url(r'^system/', include(gv.configuration.system.urls)),
    # configuration/alias
    _url(r'^alias/', include(gv.configuration.alias.urls)),
]
