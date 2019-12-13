# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url, include
import gv.configuration.user.views as user
import gv.configuration.user.ajax.urls

urlpatterns = [
    # configuration/user view/top
    url(r'^$', user.user_view_top),
    # configuration ajax
    url(r'^ajax/', include(gv.configuration.user.ajax.urls)),
]
