# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.L2.ajax.views as ajax

urlpatterns = [
    # related_packages
    url(r'^related_packages$', ajax.related_packages),
    # related_package_nodes
    url(r'^related_package_nodes$', ajax.related_package_nodes),
    # create_opinion
    url(r'^create_opinion$', ajax.create_opinion),
    # create_note
    url(r'^create_note$', ajax.create_note),
    # revoke
    url(r'^revoke$', ajax.revoke),
    # modify
    url(r'^modify$', ajax.modify),
]
