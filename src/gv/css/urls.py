# -*- coding: utf-8 -*-

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.css.views as css

urlpatterns = [
    #css change
    url(r'^change$', css.change),
]
