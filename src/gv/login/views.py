# -*- coding: utf-8 -*-
import django.contrib.auth
from django.shortcuts import render
from core.common import get_text_field_value
from ctim.constant import SESSION_EXPIRY
from gv.dashboard.views import dashboard_view_top
from gv.profile.views import change_password_top

def get_login_username(request):
    return get_text_field_value(request,'username',default_value='')
def get_login_passwrod(request):
    return get_text_field_value(request,'password',default_value='')

#ログイン画面を表示
def login_top(request):
    return render(request,'cover.html',{})

#ログイン画面から認証
def login(request):
    request.session.set_expiry(SESSION_EXPIRY)
    replace_dict = {}
    #テキストフィールドからusername/password取得
    username = get_login_username(request)
    password = get_login_passwrod(request)
    #認証
    user = django.contrib.auth.authenticate(username=username,password=password)
    if user is not None:
        #ログイン
        django.contrib.auth.login(request,user)
        if user.is_active == False:
            replace_dict['error_msg'] = 'Your account has been disabled.'
        else:
            #認証成功(初期画面のdashboardへredirect)
            if user.is_modified_password == False:
                #初回ログイン時はパスワード変更画面に飛ばす
                return change_password_top(request,msg='Please Change Your Password!!!')
            else:
                #認証成功(初期画面のdashboardへredirect)
                return dashboard_view_top(request)
    else:
        #user/passwordが一致しない
        replace_dict['error_msg'] = 'Your username or password were incorrect.'

    #エラー表示(ログイン画面へ)
    return render(request,'cover.html',replace_dict)
