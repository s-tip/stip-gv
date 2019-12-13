# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import include, url
import gv.L1.views as l1
import gv.L1.ajax.urls

urlpatterns = [
    # L1 view/top
    url(r'^$', l1.l1_view_top),
    # L1 view/download_stix
    url(r'^download_stix', l1.download_stix),
    # L1 ajax
    url(r'^ajax/', include(gv.L1.ajax.urls)),
]
