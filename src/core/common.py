import datetime
import os
import pytz
from stip.common import get_text_field_value
from core.api.rs import Ctirs
from ctirs.models import Config


def get_trim_double_quotation(s):
    return s.strip('\"')


def get_trim_first_ent_double_quotation(s):
    if s[0] == '\"' and s[-1] == '\"':
        s = s[1:-1]
    return s


def get_next_location(request):
    return get_text_field_value(request, 'next', default_value='/')


def escape_file_path(path_):
    return path_.replace('\\', '\\\\').replace('\'', '\\\'')


def get_common_replace_dict(request):
    replace_dict = {}
    stip_user = request.user
    try:
        gv_user = stip_user.gv_auth_user
    except BaseException:
        stip_user.create_gv_auth_user()
    replace_dict['user'] = gv_user
    replace_dict['stip_user'] = stip_user

    css_themas = []
    bootstrap_css_dir = Config.objects.get_config().path_bootstrap_css_dir
    for file_ in os.listdir(bootstrap_css_dir):
        if os.path.isdir(os.path.join(bootstrap_css_dir, file_)):
            if file_ != 'fonts':
                css_themas.append(file_)
    css_themas.sort()
    replace_dict['css_themas'] = css_themas
    return replace_dict


def get_package_l1_info(request, package_id):
    l1_lists_ip = []
    l1_lists_domain = []
    l1_lists_url = []
    l1_lists_sha1 = []
    l1_lists_sha256 = []
    l1_lists_sha512 = []
    l1_lists_md5 = []

    ctirs = Ctirs(request)
    l1_infos = ctirs.get_stix_file_l1_info(package_id)
    for l1_info in l1_infos:
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

    l1_type_list = [
        ('ip', l1_lists_ip),
        ('domain', l1_lists_domain),
        ('url', l1_lists_url),
        ('sha1', l1_lists_sha1),
        ('sha256', l1_lists_sha256),
        ('sha512', l1_lists_sha512),
        ('md5', l1_lists_md5),
    ]
    return l1_type_list


def stix2_str_to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc)
