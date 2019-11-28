
import datetime
from stix.core.stix_package import STIXPackage
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from core.common import get_text_field_value,get_package_l1_info
from ctim.constant import SESSION_EXPIRY
from core.api.rs import Ctirs

def get_dashboard_ajax_get_stix_counts_since_days_bar(request):
    return int(get_text_field_value(request,'since_days_bar',default_value='7'))
def get_dashboard_ajax_get_stix_counts_since_days_pie(request):
    return int(get_text_field_value(request,'since_days_pie',default_value='7'))
def get_dashboard_ajax_priority_type(request):
    return get_text_field_value(request,'priority_type',default_value='bar')
def get_package_id(request):
    return get_text_field_value(request,'package_id',default_value='')

@login_required
def get_stix_counts(request):
    request.session.set_expiry(SESSION_EXPIRY)
    #GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message' : 'Invalid HTTP method'}
        return JsonResponse(r,safe=False)
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        r = {'status': 'NG',
             'message' : 'You account is inactive.'}
        return JsonResponse(r,safe=False)
    try:
        #引数から取得する指定日数を取得する
        latest_days_bar = get_dashboard_ajax_get_stix_counts_since_days_bar(request)
        latest_days_pie = get_dashboard_ajax_get_stix_counts_since_days_pie(request)
        priority_type = get_dashboard_ajax_priority_type(request)
        #個別描画の場合の指定日数の設定
        latest_days=latest_days_bar
        if priority_type!='bar':
            latest_days=latest_days_pie

        #Ctirsクラスのインスタンスを作成
        ctirs = Ctirs(request)
        #Repository Systemに問い合わせる
        j = ctirs.get_latest_stix_count_by_community(latest_days=latest_days)

        #基準日決定
        start_date = datetime.date.today()

        #円グラフのラベル(1日ごとの日付文字列)
        bar_labels = []

        #vendor set
        vendors = []
        for item in j:
            vendors.append(item['community'])

        #棒グラフのラベル取得
        for i in reversed(range(latest_days)):
            bar_labels.append(str(start_date - datetime.timedelta(i)))

        #円グラフのラベル作成
        pie_labels = vendors

        #pie_dict初期化
        pie_dict = {}
        for vendor in vendors:
            pie_dict[vendor] = 0

        #棒グラフdatasets作成
        bar_datasets = []
        pie_dict = {}
        #Communityごとに日ごとのカウントを左から(古い方から)設定する
        for community_dict in j:
            count_list = []
            #最新順に格納されているのでリバースして
            for count_item in reversed(community_dict['count']):
                count_list.append(count_item['num'])
            community_name = community_dict['community']
            bar_data = {
                'label' :   community_name,
                'data' :   count_list
            }
            #円グラフ描画用の辞書作成
            pie_dict[community_name] = sum(count_list)
            bar_datasets.append(bar_data)

        #円グラフdatasets作成
        pie_datasets = []
        for vendor in vendors:
            pie_datasets.append(pie_dict[vendor])

        r = {}
        r['status'] = 'OK'
        r['data'] = {}
        r['data']['bar_labels'] = bar_labels
        r['data']['pie_labels'] = pie_labels
        r['data']['bar_datasets'] = bar_datasets
        r['data']['pie_datasets'] = pie_datasets
        return JsonResponse(r,safe=False)
    except:
        import traceback
        traceback.print_exc()
        r = {'status': 'NG',
             'message' : 'Server Internal Error.'}
        return JsonResponse(r,safe=False)

def get_package_info(request):
    request.session.set_expiry(SESSION_EXPIRY)
    #GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message' : 'Invalid HTTP method'}
        return JsonResponse(r,safe=False)
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        r = {'status': 'NG',
             'message' : 'You account is inactive.'}
        return JsonResponse(r,safe=False)

    try:
        #package_id取得
        package_id = get_package_id(request)
        #l1情報取得
        l1_type_list = get_package_l1_info(request, package_id)
        #description 取得
        try:
            #Ctirsクラスのインスタンスを作成
            ctirs = Ctirs(request)
            #STIXイメージ取得
            dict_ = ctirs.get_stix_file_stix(package_id)
            stix_package = STIXPackage.from_dict(dict_)
            description = stix_package.stix_header.description.value
        except:
            #エラー時は空白
            description = ''

        #返却データ
        r = {
            'status'        : 'OK',
            'description'   : description
        }
        #l1情報追加
        for l1_type in l1_type_list:
            type_,values = l1_type
            r[type_] = values
    except Exception as e:
        print('Excepton:' + str(e))
        r = {'status': 'NG',
             'message' : str(e)}
    finally:
        return JsonResponse(r,safe=False)