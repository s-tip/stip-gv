try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
import gv.css.views as css

urlpatterns = [
    # css change
    _url(r'^change$', css.change),
]
