
import libtaxii
import libtaxii.clients as clients
import libtaxii.messages_11 as tm11
import libtaxii.constants as const
from ctirs.models import Taxii as TaxiiModel

class Taxii(object):
    _SUBSCRIPTION_ID = 'ctim_graph_view'

    def __init__(self,taxii_name):
        taxii = TaxiiModel.objects.get_from_taxii_name(taxii_name)
        self._address = taxii.address
        self._port = taxii.port
        self._path = taxii.path
        self._collection_name = taxii.collection
        
        #taxii client設定
        self._client = clients.HttpClient()
        self._client.set_use_https(taxii.ssl)
        self._client.set_auth_type(clients.HttpClient.AUTH_BASIC)
        self._client.set_auth_credentials({'username': taxii.login_id, 'password': taxii.login_password})

        #SubscriptionInformatin設定
        self._subscription_information = tm11.SubscriptionInformation(
            collection_name=self._collection_name,
            subscription_id=self._SUBSCRIPTION_ID,
        )
    
    #push entry
    def push(self,content):
        cb = self._get_content_block(content)
        im = self._get_inbox_message(cb)
        im_xml = im.to_xml()
        resp = self._client.call_taxii_service2(
            self._address,
            self._path,
            const.VID_TAXII_XML_11,
            im_xml,
            port=self._port
        )
        taxii_message = libtaxii.get_message_from_http_response(resp,im.message_id)
        if taxii_message.status_type == 'SUCCESS':
            #messageがない場合のみ成功
            return '' if taxii_message.message is None else taxii_message.message
        else:
            return taxii_message.message
    
    #ContentBlock取得
    def _get_content_block(self,content):
        return tm11.ContentBlock(const.CB_STIX_XML_11,content)
    
    #InboxMessage取得
    def _get_inbox_message(self,cb):
        return tm11.InboxMessage(
            message_id=tm11.generate_message_id(),
            destination_collection_names=[self._collection_name],
            subscription_information=self._subscription_information,
            content_blocks=[cb],
            )