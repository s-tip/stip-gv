
from ctim.constant import DISPLAY_NODE_THRESHOLD
from stix.common.structured_text import StructuredText

#Alchemyのデータ形式(json)を作成するクラス
class AlchemyJsonData:
    def __init__(self):
        self._json_nodes = {}
        self._json_edges = []

    def add_json_node(self,n):
        id_ = n.get_id()
        if(id_ in self._json_nodes == True):
            return
        self._json_nodes[id_] = n

    def add_json_edge(self,e):
        for edge in self._json_edges:
            if(edge == e):
                return
        self._json_edges.append(e)

    def set_json_node_exact(self,id_):
        try:
            an = self._json_nodes[id_]
            an.set_is_exact(True)
        except KeyError:
            pass

    def set_json_node_user_language(self,_user_language):
        for node in self._json_nodes.values():
            node.set_user_language(_user_language)

    #json形式に変換して返却
    #削除確認設定が有効でかつ末端ノード数が閾値を超えた場合は None を返却する
    def get_alchemy_json(self, too_many_nodes='confirm'):
        is_redact = False
        if self.is_over_unlinked_end_nodes() == True:
            if too_many_nodes == 'confirm':
                return None        #削除確認を行うため、ここから先のJson作成を実施しない
            elif too_many_nodes == 'redact':
                is_redact = True   #間引き指定
            elif too_many_nodes == 'all':
                is_redact = False  #全データ返却
            else:
                return None        #confirmと同様

        json = {}

        #nodes情報
        json_nodes = []
        json_node_ids = []
        redact_nodes = []

        for node in self._json_nodes.values():
            #ノードを間引くか判定
            if is_redact == True:
                if self.is_end_node(node) == True:  #終端ノードか判定
                    if self.is_include_in_link(node)!=True: #リンクに含まれない
                        redact_nodes.append(node)
                        #json_nodesに追加しない
                        continue
            json_nodes.append(node.get_json())
            json_node_ids.append(node._id_)
        json['nodes'] = json_nodes
        #edges情報
        json_edges=[]
        for edge in self._json_edges:
            redact_edge = False
            #edgeの_source,_targetが間引き対象のノードか判定
            for redact_node in redact_nodes:
                if edge._source == redact_node._id_ or edge._target == redact_node._id_:
                    redact_edge = True
                    break
            if redact_edge == True:
                #json_nodesに追加しない
                continue
            if edge._source not in json_node_ids:
                print('no edge. skip (%s)' % (edge._source))
                continue
            if edge._target not in json_node_ids:
                print('no edge. skip (%s)' % (edge._target))
                continue
            json_edges.append(edge.get_json())
        json['edges'] = json_edges
        return json

    def is_over_unlinked_end_nodes(self):
        count = 0
        for node in self._json_nodes.values():
            if self.is_end_node(node) == False:
                continue      #末端ノードではない為カウントしない
            else:
                if self.is_include_in_link(node) == True:
                    continue  #関連しているノードがある為カウントしない
                else:
                    count +=1  #末端ノードとしてカウント
                    #カウントが超えた段階でTrueを返却
                    if count > DISPLAY_NODE_THRESHOLD:
                        return True
        return False

    #引数のノードがリンク要素に含まれているか判断
    def is_include_in_link(self,node):
        #Eaxct / similarの場合にTrueが設定されているためそのまま返却
        return node._is_exact

    #末端ノードか判定する
    def is_end_node(self, node):
        not_end_node_types = [
            'Header',
            'Indicators',
            'Observables',
            'Campaigns',
            'TTPs',
            'Threat_Actors',
            'Incidents',
            'Exploit_Targets',
            'Courses_Of_Action',
            'Incidents']
        if node._type in not_end_node_types:
            return False
        else:
            return True
        
    def get_alchemy_node_by_id(self,id_):
        return self._json_nodes[id_]

class AlchemyJsonBase(object):
    def get_json(self):
        raise NotImplementedError()

#AlchemyのEdge(リンク)のデータクラス
class AlchemyEdge(AlchemyJsonBase):
    _source = -1
    _target = -1
    _caption = ''
    _type= ''

    def __init__(self,source,target,caption):
        self._source = source
        self._target = target
        self._caption = caption
        self._type = caption

    def __eq__(self,obj):
        if(obj is None):
            return False
        if(isinstance(obj,AlchemyEdge) == False):
            return False
        if(obj._source is None):
            return False
        if(obj._target is None):
            return False
        return ((self._source == obj._source) and (self._target == obj._target))

    #AlchemyのNodeデータを作成する(json)
    def get_json(self):
        r = {}
        r['source'] = str(self._source)
        r['target'] = str(self._target)
        r['caption'] = str(self._caption)
        r['type'] = str(self._type)
        return r

#AlchemyのNodesのデータクラス
class AlchemyNode(AlchemyJsonBase):
    _id_ = -1
    _type = ''
    _caption = ''
    _description = ''
    _cluster = -1
    _is_exact = False
    _value = ''
    _language_contents = None
    _stix2_object = None
    _user_language = None

    def __init__(self,id_,type_,caption,description,object_=None,observable_=None,cluster=None):
        super(AlchemyNode,self).__init__()
        #1番目の引数がid
        self._id_ = id_
        #2番目がタイプ
        self._set_type(type_)
        #3番目がキャプション
        self._set_caption(caption)
        #4番目がdescription
        if(description is None):
            self._description = ''
        else:
            v = ''
            if isinstance(description,str) == True:
                #description は str (主にプログラムで決定する場合)
                v = description
            elif isinstance(description,StructuredText) == True:
                #description は StructedText (主に STIX から取得する場合)
                v = description.value

            if len(v) == 0:
                self._description = ''
            else:
                self._description = v
        #5番目がcluster
        self._cluster = cluster

    #id完全一致でequal
    def __eq__(self,obj):
        if(obj is None):
            return False
        if(isinstance(obj,AlchemyNode) == False):
            return False
        if(obj._id_ != None and obj._id_ == self._id_):
            return True
        return False

    def _set_caption(self,d):
        if(d is None):
            self._caption = ''
        else:
            self._caption = d

    def _set_type(self,d):
        self._type = d

    def set_cluster(self,cluster):
        self._cluster = cluster

    def set_is_exact(self,is_exact):
        self._is_exact = is_exact

    def get_id(self):
        return self._id_
    
    def set_value(self,value):
        self._value = value

    #AlchemyのNodeデータを作成する(json)
    def get_json(self):
        r = {}
        r['id'] = self.sanitize(str(self._id_))
        r['type'] = self.sanitize(str(self._type))
        #_caption/_descriptionはstr型
        r['caption'] = self.sanitize(self._caption)
        #description
        description = self.sanitize(self._description)
        r['stix2_object'] = self._stix2_object
        r['language_contents'] = self._language_contents
        r['user_language'] = self._user_language
        r['description'] = self.sanitize(description)
        r['cluster'] = self.sanitize(str(self._cluster))
        r['value'] = self.sanitize(self._value)
        return r

    def sanitize(self,s):
        return s
    
    def set_language_contents(self,language_contents):
        self._language_contents = language_contents

    def set_stix2_object(self,_stix2_object):
        self._stix2_object = _stix2_object

    def set_user_language(self,_user_language):
        self._user_language = _user_language

    class RelatedCampaign:
        _campaign = ''
        _related_num = -1

        def __init__(self,campaign,related_num):
            self._campaign = campaign
            self._related_num = related_num

