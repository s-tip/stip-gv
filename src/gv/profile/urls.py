# URLを正規表現で評価し、マッチングした場合の処理箇所を定義
from django.conf.urls import url
import gv.profile.views as profile

urlpatterns = [
    # profile change_password/top
    url(r'^$', profile.change_password_top),
    # profile change_password
    url(r'^change_password$', profile.change_password, name='password_modified'),
    # profile change_screen_name
    url(r'^change_screen_name$', profile.change_screen_name),
]
