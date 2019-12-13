import io
from django.shortcuts import render
from core.common import get_text_field_value, get_common_replace_dict
from gv.error.views import error_page, error_page_no_view_permission, error_page_inactive
from django.contrib.auth.decorators import login_required
from ctim.constant import SESSION_EXPIRY
from core.api.rs import Ctirs
from stix.core.stix_package import STIXPackage
from django.http.response import HttpResponse


def get_l1_page(request):
    return get_text_field_value(request, 'page', default_value=0)


def get_l1_search(request):
    return get_text_field_value(request, 'search', default_value='')


def get_l1_search_type(request):
    return get_text_field_value(request, 'search_type', default_value='')


def get_l1_package_id(request):
    return get_text_field_value(request, 'package_id', default_value='')


# L1の閲覧権限を持っているか?
def check_allow_l1_view(request):
    stip_user = request.user
    user = stip_user.gv_auth_user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    # L1ビュー閲覧許可がない場合はエラー
    if not user.is_l1_view:
        return error_page_no_view_permission(request)
    return None


@login_required
def l1_view_top(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_l1_view(request)
    if error_ is not None:
        return error_
    try:
        # サーチタイプ取得
        search_type = get_l1_search_type(request)
        replace_dict = get_common_replace_dict(request)
        # リストボックス情報取得
        replace_dict['listbox_types'] = ''
        # サーチタイプリストボックス文言
        if (search_type is not None and len(search_type) != 0):
            replace_dict['search_type'] = search_type
        # レンダリング
        return render(request, 'l1.html', replace_dict)
    except Exception:
        # エラーページ
        return error_page(request)


@login_required
def download_stix(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_l1_view(request)
    if error_ is not None:
        return error_
    try:
        # Ctirsクラスのインスタンスを作成
        ctirs = Ctirs(request)
        # package_id取得
        package_id = get_l1_package_id(request)
        # apiからcontent取得
        dict_ = ctirs.get_stix_file_stix(package_id)
        stix_package = STIXPackage.from_dict(dict_)
        # XML変換した文字列をStringIO化する(その際にUNICODEに変換)
        output = io.StringIO()
        output.write(stix_package.to_xml())
        filename = '%s.xml' % (package_id)
        # response作成
        response = HttpResponse(output.getvalue(), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
        return response
    except Exception:
        # エラーページ
        return error_page(request)
