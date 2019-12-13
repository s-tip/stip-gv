# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.configuration.system.views as system

urlpatterns = [
    # configuration/system top
    url(r'^$', system.system_view_top),
    # configuration/system modify
    url(r'^modify$', system.system_modify),
]
