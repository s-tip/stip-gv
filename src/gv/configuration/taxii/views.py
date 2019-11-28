
from django.shortcuts import render
from core.common import get_text_field_value, get_common_replace_dict
from gv.error.views import error_page, error_page_free_format
from django.contrib.auth.decorators import login_required
from ctirs.models import Taxii, Config
from ctim.constant import SESSION_EXPIRY
from gv.configuration import check_allow_configuration_view
from django.http.response import  HttpResponseForbidden

def get_configuration_taxii_create_display_name(request):
    return get_text_field_value(request,'display_name',default_value='')

def get_configuration_taxii_create_address(request):
    return get_text_field_value(request,'address',default_value='')

def get_configuration_taxii_create_port(request):
    return int(get_text_field_value(request,'port',default_value='-1'))

def get_configuration_taxii_create_path(request):
    return get_text_field_value(request,'path',default_value='')

def get_configuration_taxii_create_collection(request):
    return get_text_field_value(request,'collection',default_value='')

def get_configuration_taxii_create_login_id(request):
    return get_text_field_value(request,'login_id',default_value='')

def get_configuration_taxii_create_login_password(request):
    return get_text_field_value(request,'login_password',default_value='')

def get_configuration_taxii_create_ssl(request):
    return 'ssl' in request.POST

def get_configuration_taxii_delete_display_name(request):
    return get_text_field_value(request,'display_name',default_value='')

@login_required
def taxii_view_top(request):
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
        replace_dict['taxiis'] = Taxii.objects.all()
        #レンダリング
        return render(request,'taxii.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)

@login_required
def create_taxii(request):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    #POST以外はエラー
    if request.method != 'POST':
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
        setting_name = get_configuration_taxii_create_display_name(request)
        if(setting_name == None or len(setting_name) == 0):
            return error_page_free_format(request,'No Display Name.')
        if(len(setting_name) > 100):
            return error_page_free_format(request,'Exceeded the max length of Display Name.')

        address = get_configuration_taxii_create_address(request)
        if(address == None or len(address) == 0):
            return error_page_free_format(request,'No Address.')
        if(len(address) > 100):
            return error_page_free_format(request,'Exceeded the max length of Address.')

        try:
            port = get_configuration_taxii_create_port(request)
            if(port < 0 or port > 65535):
                return error_page_free_format(request,'Invalid port.')
        except ValueError:
                return error_page_free_format(request,'Invalid port.')

        path = get_configuration_taxii_create_path(request)
        if(path == None or len(path) == 0):
            return error_page_free_format(request,'No Path.')
        if(len(path) > 100):
            return error_page_free_format(request,'Exceeded the max length of Path.')

        collection = get_configuration_taxii_create_collection(request)
        if(collection == None or len(collection) == 0):
            return error_page_free_format(request,'No Collection.')
        if(len(collection) > 100):
            return error_page_free_format(request,'Exceeded the max length of Collection.')

        login_id = get_configuration_taxii_create_login_id(request)
        if(login_id == None or len(login_id) == 0):
            return error_page_free_format(request,'No Login ID.')
        if(len(login_id) > 100):
            return error_page_free_format(request,'Exceeded the max length of Login ID.')

        login_password = get_configuration_taxii_create_login_password(request)
        if(len(login_password) > 100):
            return error_page_free_format(request,'Exceeded the max length of Login Password.')

        ssl = get_configuration_taxii_create_ssl(request)
        #taxii作成
        Taxii.objects.create(setting_name ,
                             address=address,
                             port=port,
                             ssl=ssl,
                             path=path,
                             collection=collection,
                             login_id=login_id,
                             login_password=login_password)
        replace_dict = get_common_replace_dict(request)
        replace_dict['taxiis'] = Taxii.objects.all()
        replace_dict['info_msg'] = 'Create or Modify Success!!'
        #レンダリング
        return render(request,'taxii.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)

@login_required
def delete_taxii(request):
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
        display_name = get_configuration_taxii_delete_display_name(request)
        if(display_name == None or len(display_name) == 0):
            return error_page_free_format(request,'No Display Name.')
        taxii = Taxii.objects.get(name=display_name)
        print(Config.objects.get().default_taxii)
        if Config.objects.get().default_taxii == taxii:
            return error_page_free_format(request,'Cannot Delete A Default Taxii Setting.')
        taxii.delete()
        replace_dict = get_common_replace_dict(request)
        replace_dict['taxiis'] = Taxii.objects.all()
        replace_dict['info_msg'] = 'Delete Success!!'
        #レンダリング
        return render(request,'taxii.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)

