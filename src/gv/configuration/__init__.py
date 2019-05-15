# -*- coding: utf-8 -*-
from gv.error.views import error_page,error_page_no_view_permission, error_page_free_format, error_page_inactive

#configurationの閲覧権限を持っているか?
def check_allow_configuration_view(request):
    stip_user = request.user
    user = stip_user.gv_auth_user
    #activeユーザー以外はエラー
    if stip_user.is_active == False:
        return error_page_inactive(request)
    #L1ビュー閲覧許可がない場合はエラー
    if stip_user.is_admin == False:
        return error_page_no_view_permission(request)
    return None

