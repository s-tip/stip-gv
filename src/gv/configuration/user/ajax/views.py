# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from core.common import get_text_field_value
from django.views.decorators.csrf import csrf_protect
from ctirs.models import STIPUser
from ctim.constant import SESSION_EXPIRY

def get_configuration_user_ajax_change_auth_username(request):
    return get_text_field_value(request,'username',default_value='')
def get_configuration_user_ajax_change_auth_key(request):
    return get_text_field_value(request,'key',default_value='')
def get_configuration_user_ajax_change_auth_value(request):
    return get_text_field_value(request,'value',default_value='')

@csrf_protect
def change_auth(request):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    #GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message' : 'Invalid HTTP method'}
        return JsonResponse(r,safe=False)
    #activeユーザー以外はエラー
    if stip_user.is_active == False:
        r = {'status': 'NG',
             'message' : 'You account is inactive.'}
        return JsonResponse(r,safe=False)
    #is_staff権限なしの場合はエラー
    if stip_user.is_admin == False:
        r = {'status': 'NG',
             'message' : 'No permission.'}
        return JsonResponse(r,safe=False)

    try:
        username =  get_configuration_user_ajax_change_auth_username(request)
        key = get_configuration_user_ajax_change_auth_key(request)
        value  = True if get_configuration_user_ajax_change_auth_value(request) == u'true' else False

        u = STIPUser.objects.get(username=username).gv_auth_user
        #superユーザーの変更は不可能
        if stip_user.is_superuser == True:
            r = {'status': 'NG',
                 'message' : '%s is superuser.' % (u)}
            return JsonResponse(r,safe=False)
        #keyに応じて属性の値を変更
        if(key == u'is_l1_view'):
            u.is_l1_view = value
        elif(key == u'is_l2_view'):
            u.is_l2_view = value
        elif(key == u'is_sharing_view'):
            u.is_sharing_view = value
        #変更を保存
        u.save()
        r = {'status': 'OK',
             'message' : 'Success'}
    except Exception as e:
        r = {'status': 'NG',
             'message' : str(e)}
    finally:
        return JsonResponse(r,safe=False)

