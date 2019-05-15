# -*- coding: utf-8 -*-

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.L2.ajax.views as ajax

urlpatterns = [
    #related_packages
    url(r'^related_packages', ajax.related_packages),
    #related_package_nodes
    url(r'^related_package_nodes', ajax.related_package_nodes),
]

