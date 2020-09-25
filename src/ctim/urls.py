from django.conf.urls import include, url
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
import django.views.i18n


urlpatterns = [
    url(r'^dashboard/', include(gv.dashboard.urls)),
    url(r'^L1/', include(gv.L1.urls)),
    url(r'^L2/', include(gv.L2.urls)),
    url(r'^sharing/', include(gv.sharing.urls)),
    url(r'^configuration/', include(gv.configuration.urls)),
    url(r'^$', dashboard.dashboard_view_top),
    url(r'^login/', login, name='login'),
    url(r'^login_totp/', login_totp, name='login_totp'),
    url(r'^logout$', logout),
    url(r'^css/', include(gv.css.urls)),
    url(r'^profile/', include(gv.profile.urls)),
    url(r'^jsi18n/(?P<packages>\S+?)/$', django.views.i18n.javascript_catalog),
]
