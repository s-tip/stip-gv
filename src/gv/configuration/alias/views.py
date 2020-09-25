from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stip.common import get_text_field_value
from core.common import get_common_replace_dict
from ctirs.models import Aliases
from ctim.constant import SESSION_EXPIRY
from gv.error.views import error_page, error_page_free_format, error_page_inactive


def get_configuration_alias_create_alias(request):
    return get_text_field_value(request, 'alias', default_value='')


def get_configuration_alias_id(request):
    return get_text_field_value(request, 'id', default_value='')


# configuration(alias)の閲覧権限を持っているか?
def check_allow_configuration_alias_view(request):
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    return None


@login_required
def alias_view_top(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_configuration_alias_view(request)
    if error_ is not None:
        return error_
    try:
        replace_dict = get_common_replace_dict(request)
        # ユーザIDで絞込みしたテーブル取得
        stip_user = request.user
        replace_dict['aliases'] = Aliases.objects.filter(user=stip_user)
        # レンダリング
        return render(request, 'alias.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def create_alias(request):
    request.session.set_expiry(SESSION_EXPIRY)
    if request.method != 'POST':
        return error_page_free_format(request, 'invalid method')
    error_ = check_allow_configuration_alias_view(request)
    if error_ is not None:
        return error_
    try:
        pid = get_configuration_alias_id(request)
        setting_alias = get_configuration_alias_create_alias(request)
        if(setting_alias is None or len(setting_alias) == 0):
            return error_page_free_format(request, 'No Alias.')
        if(len(setting_alias) > 10240):
            return error_page_free_format(request, 'Exceeded the max length of Alias.')
        # alias作成
        stip_user = request.user
        Aliases.objects.create(setting_alias, stip_user, pid)
        replace_dict = get_common_replace_dict(request)
        replace_dict['aliases'] = Aliases.objects.filter(user=stip_user)
        replace_dict['info_msg'] = 'Create or Modify Success!!'
        # レンダリング
        return render(request, 'alias.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def delete_alias(request):
    request.session.set_expiry(SESSION_EXPIRY)
    if request.method != 'GET':
        return error_page_free_format(request, 'invalid method')
    error_ = check_allow_configuration_alias_view(request)
    if error_ is not None:
        return error_
    try:
        pid = get_configuration_alias_id(request)
        if(pid is None or len(pid) == 0):
            return error_page_free_format(request, 'No Id.')
        stip_user = request.user
        alias = Aliases.objects.get(pk=pid, user=stip_user)
        alias.delete()
        replace_dict = get_common_replace_dict(request)
        replace_dict['aliases'] = Aliases.objects.filter(user=stip_user)
        replace_dict['info_msg'] = 'Delete Success!!'
        # レンダリング
        return render(request, 'alias.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)
