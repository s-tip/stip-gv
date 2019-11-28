# -*- coding: utf-8 -*-
from django.shortcuts import render
from core.common import get_common_replace_dict
from gv.error.views import error_page,error_page_inactive
from ctim.constant import SESSION_EXPIRY
from core.api.rs import Ctirs

#dashboardのLATEST_CTIテーブルに表示する件数
LATEST_CTI_TABLE_NUM = 10

def dashboard_view_top(request):
    request.session.set_expiry(SESSION_EXPIRY)
    #認証されていない場合はログインページヘ
    if request.user.is_authenticated() == False:
        return render(request,'cover.html')
    
    stip_user =  request.user
    #activeユーザー以外はエラー
    if stip_user.is_active == False:
        return error_page_inactive(request)
    try:
        replace_dict = get_common_replace_dict(request)
        replace_dict['caution_msg'] = {}
        #username/passwordが'admin'の場合、password変更を促すメッセージを表示
        try:
            change_pass_flag = request.session['change_pass_flag']
        except KeyError:
            #SSO対応
            #login 画面を跳ばした場合はchange_pass_flag がない
            #caution_msg はなしとする
            change_pass_flag = False

        if change_pass_flag == True:
            replace_dict['caution_msg'] = 'Please change your administrator password from its default one.'
            request.session['change_pass_flag'] = False
        else:
            change_pass_flag = False
            replace_dict['caution_msg'] = {}

        try:
            #Ctirsクラスのインスタンスを作成
            ctirs = Ctirs(request)
            #count 情報を Repository System から取得する
            replace_dict['counts'] = ctirs.get_count_by_type()
            #最新 CTI 情報を Repository System から取得する
            replace_dict['latest_packages'] = ctirs.get_package_list(limit=10,order_by='-created')
            #レンダリング
            return render(request,'dashboard.html',replace_dict)
        except Exception:
            if ('caution_msg_ctirs_flag' in request.session) == True and request.session['caution_msg_ctirs_flag'] == True:
                #CTIRSの情報に接続できない旨通知するメッセージを表示
                replace_dict['caution_msg_ctirs'] = 'You missed the connection setting to CTIRS.'
                request.session['caution_msg_ctirs_flag'] = False
            #レンダリング
            return render(request,'dashboard.html',replace_dict)

    except Exception:
        import traceback
        traceback.print_exc()
        #エラーページ
        return error_page(request,replace_dict['caution_msg'])

