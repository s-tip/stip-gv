import traceback
import json
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponseServerError
from stip.common import get_text_field_value
from ctim.constant import SESSION_EXPIRY
from ctirs.models import Aliases
from core.api.rs import Ctirs
from core.common import stix2_str_to_datetime


# L1 Viewの閲覧権限を持っているか?
def check_allow_l1_view(request):
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        r = {'status': 'NG',
             'message': 'You account is inactive.'}
        return JsonResponse(r, safe=False)
    return None


def get_l1_ajax_create_sighting_first_seen(request):
    return get_text_field_value(request, 'first_seen', default_value='')


def get_l1_ajax_create_sighting_last_seen(request):
    return get_text_field_value(request, 'last_seen', default_value='')


def get_l1_ajax_create_sighting_count(request):
    return get_text_field_value(request, 'count', default_value='')


def get_l1_ajax_create_sighting_observed_data_id(request):
    return get_text_field_value(request, 'observed_data_id', default_value='')


@login_required
def create_sighting(request):
    request.session.set_expiry(SESSION_EXPIRY)
    # GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message': 'Invalid HTTP method'}
        return JsonResponse(r, safe=False)
    try:
        # 引数チェック
        try:
            first_seen = stix2_str_to_datetime(get_l1_ajax_create_sighting_first_seen(request))
        except BaseException:
            r = {'status': 'NG',
                 'message': 'first_seen is invalid.' % ()}
            return JsonResponse(r, safe=False)
        try:
            last_seen = stix2_str_to_datetime(get_l1_ajax_create_sighting_last_seen(request))
        except BaseException:
            r = {'status': 'NG',
                 'message': 'last_seen is invalid.' % ()}
            return JsonResponse(r, safe=False)
        try:
            count = int(get_l1_ajax_create_sighting_count(request))
        except BaseException:
            r = {'status': 'NG',
                 'message': 'count is invalid.' % ()}
            return JsonResponse(r, safe=False)

        observed_data_id = get_l1_ajax_create_sighting_observed_data_id(request)
        if len(observed_data_id) == 0:
            r = {'status': 'NG',
                 'message': 'observed_data_id is invalid.' % ()}
            return JsonResponse(r, safe=False)

        # 投稿
        ctirs = Ctirs(request)
        r = ctirs.post_stix_v2_sighting(observed_data_id, first_seen, last_seen, count)

        # Data 作成
        resp = {}
        resp['status'] = 'OK'
        resp['message'] = 'Success'
        resp['sighting_id'] = r['sighting_object_id']
        resp['json'] = r['sighting_object_json']
        return JsonResponse(resp, safe=False)
    except Exception as e:
        traceback.print_exc()
        r = {'status': 'NG',
             'message': e.message}
        return HttpResponseServerError(r)


@login_required
def get_l1_info_data_tables(request):
    request.session.set_expiry(SESSION_EXPIRY)
    # GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message': 'Invalid HTTP method'}
        return JsonResponse(r, safe=False)
    r = check_allow_l1_view(request)
    if r is not None:
        return r
    try:
        # ajax parameter取得
        sEcho = request.GET['sEcho']
        # 表示する長さ
        iDisplayLength = int(request.GET['iDisplayLength'])
        # 表示開始位置インデックス
        iDisplayStart = int(request.GET['iDisplayStart'])
        # 検索文字列
        sSearch = request.GET['sSearch']
        # ソートする列
        sort_col = int(request.GET['iSortCol_0'])
        # ソート順番 (desc指定で降順)
        sort_dir = request.GET['sSortDir_0']
        # alias設定
        aliases = []
        # DBから設定をロード
        ctim_user = request.user.gv_auth_user
        for alias in Aliases.objects.filter(user=ctim_user.id):
            # alias設定を改行コードで区切りすべてリストに追加
            aliases.append(alias.alias.split('\r\n'))

        # 文字列に変換
        aliases_str = json.dumps(aliases)

        # Ctirsクラスのインスタンスを作成
        ctirs = Ctirs(request)
        # ajax呼び出し
        data = ctirs.get_l1_info_for_l1table(iDisplayLength, iDisplayStart, sSearch, sort_col, sort_dir, aliases_str)
        if data is None:
            raise Exception('No data')

        # 返却jsonからhtmlデータ作成
        aaData = []
        for item in data['data']:
            l = []
            l.append(item['type'])
            l.append(item['value'])
            # pacakge name link
            package_name = item['package_name']
            package_id = item['package_id']
            url = '/L2/?package_id=%s' % (package_id)
            s = '<a href=\"%s\" class="l1-pacakage-name-anchor">%s</a>' % (url, package_name)
            l.append(s)
            l.append(item['title'])
            l.append(item['description'])
            l.append(item['created'])
            # sighting
            if item['stix_v2']:
                # V2 の場合は
                s = '<a class="anchor-create-sighting" observable-id="%s" observable-value="%s"><span class="glyphicon glyphicon-pencil"></span></a>' % (item['observable_id'], item['value'])
                l.append(s)
            else:
                l.append('')
            aaData.append(l)

        # Data 作成
        resp = {}
        resp['iTotalRecords'] = int(data['iTotalRecords'])
        resp['iTotalDisplayRecords'] = int(data['iTotalDisplayRecords'])
        resp['sEcho'] = sEcho
        resp['aaData'] = aaData
        return JsonResponse(resp, safe=False)
    except Exception as e:
        traceback.print_exc()
        r = {'status': 'NG',
             'message': e.message}
        return HttpResponseServerError(r)
