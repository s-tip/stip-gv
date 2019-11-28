

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.configuration.taxii.views as taxii

urlpatterns = [
    #configuration/taxii view/top
    url(r'^$', taxii.taxii_view_top),
    #configuration/taxii create_taxii
    url(r'^create_taxii$', taxii.create_taxii),
    #configuration/taxii delete_taxii
    url(r'^delete_taxii$', taxii.delete_taxii),
]
