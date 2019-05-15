# -*- coding: utf-8 -*-

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.sharing.ajax.views as ajax

urlpatterns = [
    #getrawstix
    url(r'^getrawstix$', ajax.get_raw_stix),
    #getdrawdata
    url(r'^getdrawdata$', ajax.get_draw_data),
    #send_taxi
    url(r'^send_taxii', ajax.send_taxii),
    #get_upload_stix
    url(r'^get_upload_stix', ajax.get_upload_stix),
    #change_stix_comment
    url(r'^change_stix_comment$', ajax.change_stix_comment),
    #get_stix_comment
    url(r'^get_stix_comment$', ajax.get_stix_comment),
    #get_package_table
    url(r'^get_package_table', ajax.get_package_table),
    #create_language_content
    url(r'^create_language_content', ajax.create_language_content),
]

