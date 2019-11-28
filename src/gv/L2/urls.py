

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import include,url
import gv.L2.views as l2
import gv.L2.ajax.urls

urlpatterns = [
    #L2 view/top
    url(r'^$', l2.l2_view_top),
    #L2 ajax
    url(r'^ajax/', include(gv.L2.ajax.urls)),
]
