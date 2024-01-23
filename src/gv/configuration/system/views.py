from django.shortcuts import render
from django.http.response import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from stip.common import get_text_field_value
from core.common import get_common_replace_dict
from gv.error.views import error_page, error_page_free_format
from ctirs.models import Config, Taxii
from gv.configuration import check_allow_configuration_view


def get_configuration_system_default_taxii(request):
    return get_text_field_value(request, 'upload_default_taxii', default_value='')


def get_configuration_system_sharing_policy_specifications(request):
    return get_text_field_value(request, 'upload_sharing_policy_specifications_file_path', default_value='')


def get_configuration_system_bootstrap_css_dir(request):
    return get_text_field_value(request, 'upload_bootstrap_css_dir', default_value='')


def get_configuration_system_rs_host(request):
    return get_text_field_value(request, 'rs_host', default_value='')


@login_required
def system_view_top(request):
    stip_user = request.user
    # GET以外はエラー
    if request.method != 'GET':
        return error_page_free_format(request, 'invalid method')
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return HttpResponseForbidden('Your account is inactivate.')
    # adminユーザ以外はエラー
    if not stip_user.is_admin:
        return HttpResponseForbidden('You have no permission.')
    error_ = check_allow_configuration_view(request)
    if error_ is not None:
        return error_
    try:
        # レンダリング
        return render(request, 'system.html', get_success_replace_dict(request))
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def system_modify(request):
    stip_user = request.user
    # POST以外はエラー
    if request.method != 'POST':
        return error_page_free_format(request, 'invalid method')
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return HttpResponseForbidden('Your account is inactivate.')
    # adminユーザ以外はエラー
    if not stip_user.is_admin:
        return HttpResponseForbidden('You have no permission.')
    error_ = check_allow_configuration_view(request)
    if error_ is not None:
        return error_
    try:
        default_taxii_name = get_configuration_system_default_taxii(request)
        path_sharing_policy_specifications = get_configuration_system_sharing_policy_specifications(request)
        path_bootstrap_css_dir = get_configuration_system_bootstrap_css_dir(request)
        rs_host = get_configuration_system_rs_host(request)

        # エラー発生時に更新前のデータを取得
        replace_dict = get_success_replace_dict(request)
        if(len(default_taxii_name) > 100):
            replace_dict['error_msg'] = 'Exceeded the max length of Default Taxii.'
            return render(request, 'system.html', replace_dict)
        if(path_sharing_policy_specifications is None or len(path_sharing_policy_specifications) == 0):
            replace_dict['error_msg'] = 'No Sharing Policy Specifications File Path.'
            return render(request, 'system.html', replace_dict)
        if(len(path_sharing_policy_specifications) > 100):
            replace_dict['error_msg'] = 'Exceeded the max length of Sharing Policy Specifications File Path.'
            return render(request, 'system.html', replace_dict)
        if(rs_host is None or len(rs_host) == 0):
            replace_dict['error_msg'] = 'No RS: Host.'
            return render(request, 'system.html', replace_dict)

        if(path_bootstrap_css_dir is None or len(path_bootstrap_css_dir) == 0):
            replace_dict['error_msg'] = 'No Bootstrap CSS Directory.'
            return render(request, 'system.html', replace_dict)
        if(len(path_bootstrap_css_dir) > 100):
            replace_dict['error_msg'] = 'Exceeded the max length of Bootstrap CSS Directory.'
            return render(request, 'system.html', replace_dict)

        # Config更新
        Config.objects.modify_system(default_taxii_name, path_sharing_policy_specifications, path_bootstrap_css_dir, rs_host)
        # データ更新後のデータを取得
        replace_dict = get_success_replace_dict(request)
        # レンダリング
        replace_dict['info_msg'] = 'Modify Success!!'
        return render(request, 'system.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


def get_success_replace_dict(request):
    replace_dict = get_common_replace_dict(request)
    replace_dict['config'] = Config.objects.get()
    replace_dict['taxiis'] = Taxii.objects.all()
    return replace_dict
