
from django.shortcuts import render
from core.common import get_text_field_value, get_common_replace_dict
from gv.error.views import error_page, error_page_free_format
from django.contrib.auth.decorators import login_required
from ctirs.models import STIPUser
from ctim.constant import SESSION_EXPIRY
from gv.configuration import check_allow_configuration_view
from django.http.response import HttpResponseForbidden

def get_configuration_user_create_user_username(request):
    return get_text_field_value(request,'username',default_value='')

def get_configuration_user_create_user_password(request):
    return get_text_field_value(request,'password',default_value='')

def get_configuration_user_create_user_screen_name(request):
    return get_text_field_value(request,'screen_name',default_value='')

def get_configuration_user_delete_user_username(request):
    return get_text_field_value(request,'username',default_value='')

def get_configuration_user_create_user_is_staff(request):
    return get_configuration_user_check_value(request,'is_staff')

def get_configuration_user_create_user_is_l1_view(request):
    return get_configuration_user_check_value(request,'is_l1_view')

def get_configuration_user_create_user_is_l2_view(request):
    return get_configuration_user_check_value(request,'is_l2_view')

def get_configuration_user_create_user_is_sharing_view(request):
    return get_configuration_user_check_value(request,'is_sharing_view')

def get_configuration_user_check_value(request,key):
    if (key in request.POST) == True:
        if(request.POST[key] == 'on'):
            return True
    return False

@login_required
def user_view_top(request):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    #GET以外はエラー
    if request.method != 'GET':
        return error_page_free_format(request,'invalid method')
    #activeユーザー以外はエラー
    if stip_user.is_active == False:
        return HttpResponseForbidden('Your account is inactivate.')
    #is_staff権限なしの場合はエラー
    if stip_user.is_admin == False:
        return HttpResponseForbidden('Your account is not admin.')

    error_ = check_allow_configuration_view(request)
    if error_ is not None:
        return error_ 
    try:
        replace_dict = get_common_replace_dict(request)
        gv_users = []
        for stip_user in STIPUser.objects.all():
            try:
                _ = stip_user.gv_auth_user
                gv_users.append(stip_user)
            except Exception as e:
                pass
        replace_dict['gv_users'] = gv_users
        #レンダリング
        return render(request,'user.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)

