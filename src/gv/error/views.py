import traceback
import io
from core.common import get_common_replace_dict
from django.shortcuts import render


# tracebackよりメッセージを取得し返却
def get_error_msg():
    # error情報取得
    err_io = io.StringIO()
    traceback.print_exc(None, err_io)
    err_msg = err_io.getvalue()
    err_io.close()
    return err_msg


# エラーページレンダリング
def error_page(request, caution_msg=None):
    # username/passwordが'admin'の場合、password変更を促すメッセージを取得
    out_error_msg = get_error_msg()
    print(out_error_msg)
    # error情報取得
    if caution_msg:
        err_msg = caution_msg
    else:
        err_msg = 'A system error has occurred. Please check the system log.'
    return error_page_free_format(request, err_msg, caution_msg)


# エラーページレンダリング/許可されていないページのアクセス
def error_page_no_view_permission(request):
    return error_page_free_format(request, 'You have no permission to view this page.')


# エラーページレンダリング/adminユーザーではない
def error_page_no_view_not_admin(request):
    return error_page_free_format(request, 'You have no permission.')


# エラーページレンダリング/activeユーザーではない
def error_page_inactive(request):
    return error_page_free_format(request, 'You account is inactive.')


# エラーページレンダリング/フリーフォーマット
def error_page_free_format(request, msg, caution_msg=None):
    replace_dict = get_common_replace_dict(request)
    # error情報取得
    replace_dict['err_msg'] = msg
    # username/passwordが'admin'の場合、password変更を促すメッセージを取得
    replace_dict['caution_msg'] = caution_msg
    # RequestContext作成
    return render(request, 'error.html', replace_dict)
