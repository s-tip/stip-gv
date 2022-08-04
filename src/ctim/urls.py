from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from gv.login.views import login, login_totp
from gv.logout.views import logout
import gv.dashboard.views as dashboard
import gv.dashboard.urls
import gv.L1.urls
import gv.L2.urls
import gv.sharing.urls
import gv.configuration.urls
import gv.css.urls
import gv.profile.urls
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    _url(r'^dashboard/', include(gv.dashboard.urls)),
    _url(r'^L1/', include(gv.L1.urls)),
    _url(r'^L2/', include(gv.L2.urls)),
    _url(r'^sharing/', include(gv.sharing.urls)),
    _url(r'^configuration/', include(gv.configuration.urls)),
    _url(r'^$', dashboard.dashboard_view_top),
    _url(r'^login/', login, name='login'),
    _url(r'^login_totp/', login_totp, name='login_totp'),
    _url(r'^logout$', logout),
    _url(r'^css/', include(gv.css.urls)),
    _url(r'^profile/', include(gv.profile.urls)),
    _url(r'^jsi18n/(?P<packages>\S+?)/$', JavaScriptCatalog.as_view()),
]
