from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stip.common import get_text_field_value
from gv.error.views import error_page, error_page_inactive
from core.common import get_common_replace_dict
from core.api.rs import Ctirs


def get_l2_view_top_package_id(request):
    return get_text_field_value(request, 'package_id', default_value='')


def get_l2_view_top_object_id(request):
    return get_text_field_value(request, 'object_id', default_value='')


def get_l2_view_top_ipv4_similarity(request):
    return get_text_field_value(request, 'similarity_ipv4', default_value='')


def get_l2_view_top_domain_similarity(request):
    return get_text_field_value(request, 'similarity_domain', default_value='')


def check_allow_l2_view(request):
    stip_user = request.user
    if not stip_user.is_active:
        return error_page_inactive(request)
    return None


@login_required
def l2_view_top(request):
    error_ = check_allow_l2_view(request)
    if error_ is not None:
        return error_
    try:
        package_id = get_l2_view_top_package_id(request)
        ipv4 = get_l2_view_top_ipv4_similarity(request)
        domain = get_l2_view_top_domain_similarity(request)
        replace_dict = get_common_replace_dict(request)
        object_id = get_l2_view_top_object_id(request)

        ctirs = Ctirs(request)
        if len(package_id) == 0 and len(object_id) != 0:
            try:
                bundles = ctirs.get_bundle_from_object_id(object_id)['package_id_list']
                package_id = bundles[0]
            except Exception:
                package_id = ''
        packages = ctirs.get_package_list()
        replace_dict['packages'] = packages
        replace_dict['package_id'] = package_id
        replace_dict['ipv4'] = ipv4
        replace_dict['domain'] = domain
        return render(request, 'l2.html', replace_dict)
    except Exception:
        import traceback
        traceback.print_exc()
        return error_page(request)
