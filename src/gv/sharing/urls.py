

#URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import include,url
import gv.sharing.views as sharing
import gv.sharing.ajax.urls

urlpatterns = [
    #Sharing view/top
    url(r'^$', sharing.sharing_view_top),
    #stix_upload更新
    url(r'^stix_upload$', sharing.stix_upload),
    #download
    url(r'^stix_download$', sharing.stix_download),
    #csv-download
    url(r'^stix_data_csv_download$', sharing.stix_data_csv_download),
    #delete package
    url(r'^delete_package$', sharing.delete_package),
    #sharing ajax
    url(r'^ajax/', include(gv.sharing.ajax.urls)),
]
