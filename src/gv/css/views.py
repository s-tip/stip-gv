from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from stip.common import get_text_field_value
from core.common import get_next_location
from gv.error.views import error_page, error_page_inactive
from ctim.constant import SESSION_EXPIRY


def get_css_change_css_thema(request):
    return get_text_field_value(request, 'css_thema', default_value='default')


@login_required
def change(request):
    request.session.set_expiry(SESSION_EXPIRY)
    # activeユーザー以外はエラー
    if not request.user.is_active:
        return error_page_inactive(request)
    try:
        # cssの変更を保存
        stip_user = request.user
        user = stip_user.gv_auth_user
        user.css_thema = get_css_change_css_thema(request)
        user.save()
        return redirect('/')
    except Exception:
        # エラーページ
        return error_page(request)
