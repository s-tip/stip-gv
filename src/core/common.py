
import os
import datetime
import pytz
from django.utils.datastructures import MultiValueDictKeyError
from ctirs.models import Config
from core.api.rs import Ctirs

def get_trim_double_quotation(s):
    return s.strip('\"')

#前後のダブルクォーテーションのみ除去
def get_trim_first_ent_double_quotation(s):
    if s[0]=='\"' and s[-1]=='\"':
        s=s[1:-1]
    return s

#textfieldからitem_name指定の値を取得。未定義時はdefault_value
def get_text_field_value(request,item_name,default_value=None,is_trim_end_space=False):
    if request.method == 'GET':
        l = request.GET
    elif request.method == 'POST':
        l = request.POST
    else:
        return default_value
    try:
        v = l[item_name]
        if len(v) == 0:
            return default_value
        else:
            #is_trim_end_spaceがFalse以外の場合は前後の空白を取り除かない
            if(is_trim_end_space is not False):
                return v
            else:
                #テキストフィールドから取得する場合は前後の空白は取り除く
                return v.strip()
    except MultiValueDictKeyError:
        return default_value

#同じページを返却する場合のlocationを取得する(デフォルトは/)
def get_next_location(request):
    return get_text_field_value(request,'next',default_value='/')

#ファイルパスをescapeする
def escape_file_path(path_):
    return path_.replace('\\', '\\\\').replace('\'', '\\\'')

#CTIM画面の共通replace辞書取得
def get_common_replace_dict(request):
    #config = Config.objects.get_config()
    replace_dict = {}
    #ヘッダのユーザー情報
    stip_user = request.user
    try:
        gv_user = stip_user.gv_auth_user
    except:
        #gv_auth_user が見つからないので作成して保存する
        stip_user.create_gv_auth_user()
    replace_dict['user']  = gv_user
    replace_dict['stip_user']  = stip_user

    #css_themaの一覧を取得
    css_themas = []
    bootstrap_css_dir = Config.objects.get_config().path_bootstrap_css_dir
    for file_ in os.listdir(bootstrap_css_dir):
        if os.path.isdir(os.path.join(bootstrap_css_dir,file_)) == True:
            #fontsディレクトリは除外
            if file_ != 'fonts':
                css_themas.append(file_)
    #css_themasをアルファベット順にソート
    css_themas.sort()
    replace_dict['css_themas']  = css_themas
    return replace_dict

def get_package_l1_info(request,package_id):
    l1_lists_ip = []
    l1_lists_domain = []
    l1_lists_url = []
    l1_lists_sha1 = []
    l1_lists_sha256 = []
    l1_lists_sha512 = []
    l1_lists_md5 = []

    #Ctirsクラスのインスタンスを作成
    ctirs = Ctirs(request)
    #REST API で L1情報取得する
    l1_infos = ctirs.get_stix_file_l1_info(package_id)
    for l1_info in  l1_infos:
        type_ = l1_info['type']
        value = l1_info['value']
        if type_ == 'ipv4':
            l1_lists_ip.append(value)
        elif type_ == 'domain_name':
            l1_lists_domain.append(value)
        elif type_ == 'uri':
            l1_lists_url.append(value)
        elif type_ == 'sha1':
            l1_lists_sha1.append(value)
        elif type_ == 'sha256':
            l1_lists_sha256.append(value)
        elif type_ == 'sha512':
            l1_lists_sha512.append(value)
        elif type_ == 'md5':
            l1_lists_md5.append(value)
                
    #情報を連結する
    l1_type_list = [
        ('ip'       ,   l1_lists_ip),
        ('domain'   ,   l1_lists_domain),
        ('url'      ,   l1_lists_url),
        ('sha1'     ,   l1_lists_sha1),
        ('sha256'   ,   l1_lists_sha256),
        ('sha512'   ,   l1_lists_sha512),
        ('md5'      ,   l1_lists_md5),
    ]
    return l1_type_list

#STIX2 で使われる時間文字列から datetime に変換する
def stix2_str_to_datetime(s):
    return datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc)