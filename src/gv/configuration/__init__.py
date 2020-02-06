from gv.error.views import error_page, error_page_no_view_not_admin, error_page_free_format, error_page_inactive


# configurationの閲覧権限を持っているか?
def check_allow_configuration_view(request):
    stip_user = request.user
    # activeユーザー以外はエラー
    if not stip_user.is_active:
        return error_page_inactive(request)
    # adminユーザ以外はエラー
    if not stip_user.is_admin:
        return error_page_no_view_not_admin(request)
    return None
