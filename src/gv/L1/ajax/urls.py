# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.L1.ajax.views as ajax

urlpatterns = [
    url(r'^get_l1_info_data_tables', ajax.get_l1_info_data_tables),
    url(r'^create_sighting', ajax.create_sighting),
]
