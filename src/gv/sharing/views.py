import os
import io
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from core.policy.policy import get_policy_communities
from core.common import get_text_field_value, get_common_replace_dict, get_package_l1_info
from core.api.rs import Ctirs
from gv.sharing.ajax.views import save_redacted_stix_file
from gv.error.views import error_page, error_page_no_view_permission, error_page_inactive, error_page_free_format
from ctirs.models import Taxii, Config
from ctim.constant import SESSION_EXPIRY
from stip.common.const import LANGUAGES


# filefieldからitem_name指定の値を取得。未定義時はNone
# list形式で返却
def get_file_field_value(request, item_name):
    try:
        return request.FILES.getlist(item_name)
    except MultiValueDictKeyError:
        return None


# STIXファイル取得/指定無時はNone/リストで返却される
def get_sharing_stix(request):
    return get_file_field_value(request, 'stix')


def get_sharing_upload_package_name(request):
    return get_text_field_value(request, 'upload_package_name', default_value='')


def get_sharing_upload_vendor_id(request):
    return get_text_field_value(request, 'upload_vendor_id', default_value=None)


def get_sharing_csv_download_package_id(request):
    return get_text_field_value(request, 'package_id', default_value=None)


def get_sharing_delete_package_package_id(request):
    return get_text_field_value(request, 'package_id', default_value='')


# 入力検体をtemp書き込み/ファイル名は変更してはいけない
def write_temp_stix(request):
    stixes = get_sharing_stix(request)
    if len(stixes) != 1:
        # stix指定個数が1以外は無効
        return None

    # 最初の要素のみを対象
    stix = stixes[0]

    stix_dir = Config.objects.get_config().path_upload_stix_dir
    stix_file_path = stix_dir + os.sep + stix.name

    stix_file_path_str = stix_file_path
    if os.name == 'posix':
        stix_file_path_str = stix_file_path
    # 同名のファイルを削除する
    try:
        os.remove(stix_file_path_str)
    except BaseException:
        pass

    with open(stix_file_path_str, 'wb+') as fp:
        for chunk in stix:
            fp.write(chunk)
    return stix_file_path


# Sharing Viewの閲覧権限を持っているか?
def check_allow_sharing_view(request):
    stip_user = request.user
    user = stip_user.gv_auth_user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    # sharingビュー閲覧許可がない場合はエラー
    if not user.is_sharing_view:
        return error_page_no_view_permission(request)
    return None


@login_required
def sharing_view_top(request, info_msg=''):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_sharing_view(request)
    if error_ is not None:
        return error_
    try:
        replace_dict = get_common_replace_dict(request)

        # Poclicyファイルからcommunity一覧を取得
        communities = get_policy_communities().split(',')
        # policyセット(tableのheader部で使用)
        replace_dict['communities'] = communities
        # TAXII
        replace_dict['taxiis'] = Taxii.objects.all()
        # config
        replace_dict['config'] = Config.objects.get()
        # message
        replace_dict['info_msg'] = info_msg
        # languages
        replace_dict['languages'] = LANGUAGES
        # languages
        replace_dict['user'] = request.user
        try:
            # Ctirsクラスのインスタンスを作成
            ctirs = Ctirs(request)
            # rs_communities (Vendor Source)
            replace_dict['rs_communities'] = ctirs.get_rs_communities()
        except Exception:
            # レンダリング
            return render(request, 'sharing.html', replace_dict)
        # レンダリング
        return render(request, 'sharing.html', replace_dict)
    except Exception:
        return error_page(request)

# stix upload
@csrf_protect
@login_required
def stix_upload(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_sharing_view(request)
    if error_ is not None:
        return error_
    try:
        # post以外はエラー
        if request.method != 'POST':
            # エラー画面
            raise Exception('Invalid HTTP Method')

        package_name = get_sharing_upload_package_name(request)
        if(len(package_name) > 100):
            return error_page_free_format(request, 'Exceeded the max length of Package name.')
        community_id = get_sharing_upload_vendor_id(request)
        if(community_id is not None and len(community_id) > 100):
            return error_page_free_format(request, 'Exceeded the max length of Vendor id.')
        stixes = get_sharing_stix(request)
        # Ctirsクラスのインスタンスを作成
        ctirs = Ctirs(request)
        ctirs.post_stix_files(community_id, package_name, stixes[0])
        # レンダリング(sharingのトップページ)
        return sharing_view_top(request, 'Upload Success!!')
    except Exception:
        return error_page(request)


@csrf_protect
@login_required
def stix_download(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_sharing_view(request)
    if error_ is not None:
        return error_
    # redactedファイルを作成し、中身とファイル名を取得
    _, contents, filename = save_redacted_stix_file(request)
    # XML変換した文字列をStringIO化する
    output = io.StringIO()
    if isinstance(contents, str):
        output.write(str(contents, 'utf-8'))
    elif isinstance(contents, str):
        output.write(contents)
    # response作成
    response = HttpResponse(output.getvalue(), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
    return response


@csrf_protect
@login_required
def stix_data_csv_download(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_sharing_view(request)
    if error_ is not None:
        return error_
    try:
        # requestから値取得
        package_id = get_sharing_csv_download_package_id(request)
        if(package_id is None or len(package_id) == 0):
            return error_page_free_format(request, 'No package_id.')
        l1_type_list = get_package_l1_info(request, package_id)

        # ファイルの中身を作成する
        contents = ''
        for l1_list in l1_type_list:
            type_, l_ = l1_list
            for value in l_:
                contents += '%s,%s\n' % (type_, value)

        # ダウンロードファイル名を生成
        filename = package_id + '_observables.csv'

        # CSVデータをStringIO化する
        output = io.StringIO()
        output.write(contents)
        # response作成
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
        return response

    except Exception:
        return error_page(request)


@csrf_protect
def delete_package(request):
    request.session.set_expiry(SESSION_EXPIRY)
    error_ = check_allow_sharing_view(request)
    if error_ is not None:
        return error_
    try:
        # package ID取得
        package_ids = get_sharing_delete_package_package_id(request).split(',')
        # REST API 経由で Repository Systeに削除要求
        for package_id in package_ids:
            # Ctirsクラスのインスタンスを作成
            ctirs = Ctirs(request)
            ctirs.delete_stix_files_id(package_id)
        return sharing_view_top(request, 'Delete Success!!')
    except Exception:
        import traceback
        traceback.print_exc()
        return error_page(request)
