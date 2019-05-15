# -*- coding: utf-8 -*-

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.configuration.alias.views as alias

urlpatterns = [
    url(r'^$', alias.alias_view_top),
    url(r'^create_alias$', alias.create_alias),
    url(r'^delete_alias$', alias.delete_alias),
]
