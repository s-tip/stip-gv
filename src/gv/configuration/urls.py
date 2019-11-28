

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url, include
import gv.configuration.user.urls
import gv.configuration.taxii.urls
import gv.configuration.system.urls
import gv.configuration.alias.urls

urlpatterns = [
    #configuration/User
    url(r'^user/', include(gv.configuration.user.urls)),
    #configuration/taxii
    url(r'^taxii/', include(gv.configuration.taxii.urls)),
    #configuration/system
    url(r'^system/', include(gv.configuration.system.urls)),
    #configuration/alias
    url(r'^alias/', include(gv.configuration.alias.urls)),
]
