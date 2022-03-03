import requests
from ctirs.models import Config


class Ctirs(object):
    def __init__(self, request):
        try:
            # コンストラクタでrequestから設定を抽出し
            stip_user = request.user
            config = Config.objects.get_config()
            self.ctirs_username = stip_user.username
            self.ctirs_apikey = stip_user.api_key
            self.ctirs_host = config.ctirs_host
        except Exception:
            self.ctirs_username = ''
            self.ctirs_apikey = ''
            self.ctirs_host = ''
            import traceback
            traceback.print_exc()

    def get_rest_api_headers(self):
        headers = {
            'username': self.ctirs_username,
            'apikey': self.ctirs_apikey, }
        return headers

    # get : /api/v1/gv/l1_info_for_l1table
    def get_l1_info_for_l1table(self, iDisplayLength, iDisplayStart, sSearch, sort_col, sort_dir, aliases=[]):
        params = {
            'iDisplayLength': iDisplayLength,
            'iDisplayStart': iDisplayStart,
            'sSearch': sSearch,
            'iSortCol': sort_col,
            'sSortDir': sort_dir,
            'aliases': aliases,
        }
        url = '/api/v1/gv/l1_info_for_l1table'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/package_list
    def get_package_list(self, required_comment=False, limit=None, order_by=None):
        params = {
            'required_comment': required_comment
        }
        # limit の指定があったら付け加える
        if limit is not None:
            params['limit'] = limit
        # order_by の指定があったら付け加える
        if order_by is not None:
            params['order_by'] = order_by
        url = '/api/v1/gv/package_list'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/package_name_list
    def get_package_name_list(self, limit=None):
        params = {}
        # limit の指定があったら付け加える
        if limit is not None:
            params['limit'] = limit
        url = '/api/v1/gv/package_name_list'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/matched_packages
    def get_matched_packages(self, base_package, exact, is_ip_similar_check, is_domain_similar_check):
        # 問い合わせオプション作成
        params = {
            'package_id': base_package,
            'exact': exact,
            'similar_ipv4': is_ip_similar_check,
            'similar_domain': is_domain_similar_check
        }
        url = '/api/v1/gv/matched_packages'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/contents_and_edges
    def get_contents_and_edges(self, base_package, exact, compared_package_ids, is_ip_similar_check, is_domain_similar_check):
        # 問い合わせオプション作成
        params = {
            'package_id': base_package,
            'compared_package_ids': compared_package_ids,
            'exact': exact,
            'similar_ipv4': is_ip_similar_check,
            'similar_domain': is_domain_similar_check
        }
        url = '/api/v1/gv/contents_and_edges'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/package_list_for_sharing_table
    def get_package_list_for_sharing_table(self, iDisplayLength, iDisplayStart, sSearch, sort_col, sort_dir):
        params = {
            'iDisplayLength': iDisplayLength,
            'iDisplayStart': iDisplayStart,
            'sSearch': sSearch,
            'iSortCol': sort_col,
            'sSortDir': sort_dir,
        }
        url = '/api/v1/gv/package_list_for_sharing_table'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/stix_files/<package_id>
    def get_stix_file(self, package_id):
        params = {}
        url = '/api/v1/gv/stix_files/%s' % (package_id)
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # put : /api/v1/gv/stix_files/<package_id>/comment
    def put_stix_comment(self, package_id, comment):
        params = {
            'comment': comment
        }
        url = '/api/v1/gv/stix_files/%s/comment' % (package_id)
        # ajax呼び出し
        self._call_put_ctirs_api(url, params)
        # 戻り値はなし
        return

    # get : /api/v1/gv/stix_files/<package_id>/l1_info
    def get_stix_file_l1_info(self, package_id):
        params = {}
        url = '/api/v1/gv/stix_files/%s/l1_info' % (package_id)
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/stix_files/<package_id>/stix
    def get_stix_file_stix(self, package_id):
        params = {}
        url = '/api/v1/gv/stix_files/%s/stix' % (package_id)
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get : /api/v1/gv/communities
    def get_rs_communities(self):
        params = {}
        url = '/api/v1/gv/communities'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # post /api/v1/stix_files
    def post_stix_files(self, community_id, package_name, file_):
        params = {
            'community_id': community_id,
            'package_name': package_name
        }
        files = {
            'stix': file_
        }
        url = '/api/v1/stix_files'
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params, files=files)

    # delete /api/v1/gv/stix_file/<package_id>
    # stix_file 削除
    def delete_stix_files_id(self, package_id):
        params = {}
        url = '/api/v1/gv/stix_files/%s' % (package_id)
        # ajax呼び出し
        self._call_delete_ctirs_api(url, params)
        # 戻り値なし
        return

    # get /api/v1/gv/count_by_type
    # 種別毎の末端ノード数を取得
    def get_count_by_type(self):
        params = {}
        url = '/api/v1/gv/count_by_type'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # get /api/v1/gv/latest_stix_count_by_community
    # 1日ごとの各コミュニティーごとのファイル数を返却する
    # default は 7 日
    def get_latest_stix_count_by_community(self, latest_days=7):
        params = {
            'latest_days': latest_days,
        }
        url = '/api/v1/gv/latest_stix_count_by_community'
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # post : /api/v1/stix_files_v2/<observed_data_id>/sighting
    def post_stix_v2_sighting(self, observed_data_id, first_seen, last_seen, count):
        params = {}
        if first_seen is not None:
            params['first_seen'] = first_seen
        if last_seen is not None:
            params['last_seen'] = last_seen
        if count is not None:
            params['count'] = count
        url = '/api/v1/stix_files_v2/%s/sighting' % (observed_data_id)
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params)

    # get : /api/v1/stix_files_v2/<object_ref>/language_contents
    def get_language_contents(self, object_ref, modified):
        # 問い合わせオプション作成
        params = {
            'object_modified': modified
        }
        url = '/api/v1/stix_files_v2/%s/language_contents' % (object_ref)
        # ajax呼び出し
        return self._call_get_ctirs_api(url, params)

    # post : /api/v1/stix_files_v2/<object_ref>/language_contents
    def post_language_contents(self, object_ref, language_contents):
        # 問い合わせオプション作成
        params = {}
        j = {
            'language_contents': language_contents,
        }
        url = '/api/v1/stix_files_v2/%s/language_contents' % (object_ref)
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params, json=j)

    # get : /api/v1/stix_files_v2/search_bundle
    def get_bundle_from_object_id(self, object_id):
        params = {
            'match[object_id]': object_id
        }
        url = '/api/v1/stix_files_v2/search_bundle'
        return self._call_get_ctirs_api(url, params)

    # post /api/v1/stix_files_v2/note
    def post_note(self, object_id, content, abstract):
        params = {
            'object_id': object_id,
            'content': content,
            'abstract': abstract
        }
        url = '/api/v1/stix_files_v2/create_note'
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params, files=None)

    # post /api/v1/stix_files_v2/opinion
    def post_opinion(self, object_id, opinion, explanation):
        params = {
            'object_id': object_id,
            'opinion': opinion,
            'explanation': explanation
        }
        url = '/api/v1/stix_files_v2/create_opinion'
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params, files=None)

    # post /api/v1/stix_files_v2/revoke
    def post_revoke(self, object_id):
        params = {
            'object_id': object_id,
        }
        url = '/api/v1/stix_files_v2/revoke'
        # ajax呼び出し
        return self._call_post_ctirs_api(url, params, files=None)

    # post /api/v1/stix_files_v2/modify
    def post_modify(self, stix2):
        url = '/api/v1/stix_files_v2/modify'
        # ajax呼び出し
        return self._call_post_ctirs_api(url, {}, files=None, json=stix2)

    # ajax呼び出し(get)
    def _call_get_ctirs_api(self, url_suffix, params):
        # 共通呼び出し
        response = self._call_ctirs_api(url_suffix, params, 'GET')
        j = response.json()
        # statusがない場合はエラー
        if 'return_code' not in j:
            raise Exception('No return_code')
        # statusが0以外はエラー
        if j['return_code'] != '0':
            if 'userMessage' not in j:
                raise Exception('Error has occured. No message.')
            else:
                raise Exception('Error has occured. %s' % j['userMessage'])
        # dataがない場合は None
        if 'data' not in j:
            return None
        # 200以外はエラー
        if response.status_code is not 200:
            raise Exception('Error has occured. CTIRS REST api HTTP Response (%d).' % (response.status_code))
        # 存在する場合はj['data']を返却する
        return j['data']

    # ajax呼び出し(put)
    def _call_put_ctirs_api(self, url_suffix, params):
        # 共通呼び出し
        response = self._call_ctirs_api(url_suffix, params, 'PUT')
        # 204以外はエラー
        if response.status_code is not 204:
            raise Exception('Error has occured. CTIRS REST api HTTP Response (%d).' % (response.status_code))
        return

    # ajax呼び出し(post)
    def _call_post_ctirs_api(self, url_suffix, params, files=None, json=None):
        # 共通呼び出し
        response = self._call_ctirs_api(url_suffix, params, 'POST', files, json)
        j = response.json()
        # statusがない場合はエラー
        if 'return_code' not in j:
            raise Exception('No return_code')
        # statusが0以外はエラー
        if j['return_code'] != '0':
            if 'userMessage' in j:
                raise Exception('Error has occured. %s' % j['userMessage'])
            else:
                raise Exception('Error has occured. No message.')
        # dataがない場合は None
        if 'data' not in j:
            return None
        if response.status_code is not 201:
            raise Exception('Error has occured. CTIRS REST api HTTP Response (%d).' % (response.status_code))

        # 存在する場合はj['data']を返却する
        return j['data']

    # ajax呼び出し(delete)
    def _call_delete_ctirs_api(self, url_suffix, params):
        # 共通呼び出し
        response = self._call_ctirs_api(url_suffix, params, 'DELETE')
        # 204以外はエラー
        if response.status_code is not 204:
            raise Exception('Error has occured. CTIRS REST api HTTP Response (%d).' % (response.status_code))
        return

    # ajax呼び出し(共通)
    def _call_ctirs_api(self, url_suffix, params, method, files=None, json=None):
        # URL
        url = '%s%s' % (self.ctirs_host, url_suffix)
        # headers
        headers = self.get_rest_api_headers()
        # request
        if method == 'GET':
            response = requests.get(
                url,
                headers=headers,
                params=params,
                verify=False)
        elif method == 'PUT':
            response = requests.put(
                url,
                headers=headers,
                params=params,
                verify=False)
        elif method == 'POST':
            if json is None:
                response = requests.post(
                    url,
                    headers=headers,
                    data=params,
                    files=files,
                    verify=False)
            else:
                response = requests.post(
                    url,
                    headers=headers,
                    json=json,
                    verify=False)
        elif method == 'DELETE':
            response = requests.delete(
                url,
                headers=headers,
                params=params,
                verify=False)
        return response
