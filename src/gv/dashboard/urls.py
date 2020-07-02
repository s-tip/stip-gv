# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url, include
import gv.dashboard.views as dashboard
import gv.dashboard.ajax.urls

urlpatterns = [
    # dashboard view/top
    url(r'^$', dashboard.dashboard_view_top, name='dashboard'),
    # dashboard ajax
    url(r'^ajax/', include(gv.dashboard.ajax.urls)),
]
