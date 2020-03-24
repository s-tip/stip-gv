from django.shortcuts import render
from core.common import get_common_replace_dict
from gv.error.views import error_page, error_page_inactive
from django.contrib.auth.decorators import login_required
from ctim.constant import SESSION_EXPIRY
from core.common import get_text_field_value
from core.api.rs import Ctirs


def get_l2_view_top_package_id(request):
    return get_text_field_value(request, 'package_id', default_value='')


def get_l2_view_top_ipv4_similarity(request):
    return get_text_field_value(request, 'similarity_ipv4', default_value='')


def get_l2_view_top_domain_similarity(request):
    return get_text_field_value(request, 'similarity_domain', default_value='')


# L2の閲覧権限を持っているか?
def check_allow_l2_view(request):
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    return None


@login_required
def l2_view_top(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_l2_view(request)
    if error_ is not None:
        return error_
    try:
        # パラメタが指定されている場合は取得
        package_id = get_l2_view_top_package_id(request)
        ipv4 = get_l2_view_top_ipv4_similarity(request)
        domain = get_l2_view_top_domain_similarity(request)
        replace_dict = get_common_replace_dict(request)
        try:
            # Ctirsクラスのインスタンスを作成
            ctirs = Ctirs(request)
            # ajax呼び出し
            packages = ctirs.get_package_list()
            replace_dict['packages'] = packages
            replace_dict['package_id'] = package_id
            replace_dict['ipv4'] = ipv4
            replace_dict['domain'] = domain
            return render(request, 'l2.html', replace_dict)
        except Exception:
            # レンダリング
            return render(request, 'l2.html', replace_dict)
    except Exception:
        return error_page(request)
