from django.shortcuts import render
from core.common import get_text_field_value, get_common_replace_dict
from gv.error.views import error_page, error_page_inactive
from django.contrib.auth.decorators import login_required
from ctim.constant import SESSION_EXPIRY
from ctirs.models import STIPUser


def get_profile_change_password_old_password(request):
    return get_text_field_value(request, 'old_password', default_value='')


def get_profile_change_password_new_password(request):
    return get_text_field_value(request, 'new_password', default_value='')


def get_profile_change_screen_name_screen_name(request):
    return get_text_field_value(request, 'screen_name', default_value='')


@login_required
def change_password_top(request, msg=None):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    try:
        replace_dict = get_common_replace_dict(request)
        if msg is not None:
            replace_dict['error_change_password_msg'] = msg
        # レンダリング
        return render(request, 'profile.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def change_password(request):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    try:
        replace_dict = get_common_replace_dict(request)
        old_password = get_profile_change_password_old_password(request)
        new_password = get_profile_change_password_new_password(request)
        # 古いパスワードが正しいかチェック
        if not stip_user.check_password(old_password):
            # 古いパスワードが間違っている
            replace_dict['error_change_password_msg'] = 'Old Password is wrong!!'
            return render(request, 'profile.html', replace_dict)

        if(new_password is None or len(new_password) == 0):
            replace_dict['error_change_password_msg'] = 'No New Password.'
            return render(request, 'profile.html', replace_dict)
        if(len(new_password) > 30):
            replace_dict['error_change_password_msg'] = 'Exceeded the max length of New Password.'
            return render(request, 'profile.html', replace_dict)

        # 新しいパスワードに変更
        stip_user.set_password(new_password)
        if stip_user.username == 'admin':
            # build_in account のパスワード変更
            STIPUser.change_build_password(new_password)
        stip_user.is_modified_password = True
        stip_user.save()
        # レンダリング
        return render(request, 'change_password_done.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def change_screen_name(request):
    request.session.set_expiry(SESSION_EXPIRY)
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    try:
        replace_dict = get_common_replace_dict(request)
        screen_name = get_profile_change_screen_name_screen_name(request)
        if(screen_name is None):
            replace_dict['error_change_screen_msg'] = 'No Screen Name.'
            return render(request, 'profile.html', replace_dict)
        if(len(screen_name) == 0):
            # スクリーン名長が0
            return render(request, 'profile.html', replace_dict)
        if(len(screen_name) > 30):
            replace_dict['error_change_screen_msg'] = 'Exceeded the max length of Screen Name.'
            return render(request, 'profile.html', replace_dict)
        stip_user.screen_name = screen_name
        stip_user.save()
        replace_dict['info_change_screen_msg'] = 'Change Screen Name Success!!'
        # レンダリング
        return render(request, 'profile.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)
