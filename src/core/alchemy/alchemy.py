from ctim.constant import DISPLAY_NODE_THRESHOLD
from stix.common.structured_text import StructuredText


class AlchemyJsonData:
    def __init__(self):
        self._json_nodes = {}
        self._json_edges = []

    def add_json_node(self, n):
        id_ = n.get_id()
        if(id_ in self._json_nodes):
            return
        self._json_nodes[id_] = n

    def add_json_edge(self, e):
        self._json_edges.append(e)

    def set_json_node_exact(self, id_):
        try:
            an = self._json_nodes[id_]
            an.set_is_exact(True)
        except KeyError:
            pass

    def set_json_node_user_language(self, _user_language):
        for node in self._json_nodes.values():
            node.set_user_language(_user_language)

    def get_alchemy_json(self, ctirs, too_many_nodes='confirm'):
        is_redact = False
        if self.is_over_unlinked_end_nodes():
            if too_many_nodes == 'confirm':
                return None
            elif too_many_nodes == 'redact':
                is_redact = True
            elif too_many_nodes == 'all':
                is_redact = False
            else:
                return None

        json = {}

        json_nodes = []
        json_node_ids = []
        redact_nodes = []

        for node in self._json_nodes.values():
            if is_redact:
                if self.is_end_node(node):
                    if not self.is_include_in_link(node):
                        redact_nodes.append(node)
                        continue
            json_nodes.append(node.get_json(ctirs))
            json_node_ids.append(node._id_)
        json['nodes'] = json_nodes
        json_edges = []
        for edge in set(self._json_edges):
            redact_edge = False
            for redact_node in redact_nodes:
                if edge._source == redact_node._id_ or edge._target == redact_node._id_:
                    redact_edge = True
                    break
            if redact_edge:
                continue
            if edge._source not in json_node_ids:
                print('no edge. skip (%s)' % (edge._source))
                continue
            if edge._target not in json_node_ids:
                print('no edge. skip (%s)' % (edge._target))
                continue
            json_edges.append(edge.get_json(ctirs))
        json['edges'] = json_edges
        return json

    def is_over_unlinked_end_nodes(self):
        count = 0
        for node in self._json_nodes.values():
            if not self.is_end_node(node):
                continue
            else:
                if self.is_include_in_link(node):
                    continue
                else:
                    count += 1
                    if count > DISPLAY_NODE_THRESHOLD:
                        return True
        return False

    def is_include_in_link(self, node):
        return node._is_exact

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

    def get_alchemy_node_by_id(self, id_):
        return self._json_nodes[id_]


class AlchemyJsonBase(object):
    def get_json(self, ctirs):
        raise NotImplementedError()


class AlchemyEdge(AlchemyJsonBase):
    _id_ = None
    _source = -1
    _target = -1
    _caption = ''
    _type = ''
    _stix2_object = None

    def __init__(self, source, target, caption, type=None, object_=None):
        if object_ is not None:
            self._id_ = object_['id']
            self._stix2_object = object_
        self._source = source
        self._target = target
        self._caption = caption
        if type is None:
            self._type = caption
        else:
            self._type = type

    def __eq__(self, obj):
        return ((self._source == obj._source) and (self._target == obj._target))

    def __hash__(self):
        return hash((self._source, self._target))

    def get_json(self, ctirs):
        r = {}
        r['revoked'] = False
        r['is_updated'] = False
        if self._stix2_object is not None:
            r['id'] = self._id_
            r['stix2_object'] = self._stix2_object
            ret = ctirs.get_latest_object(
                self._stix2_object['id'],
                self._stix2_object['modified'])
            r['modified'] = self._stix2_object['modified']
            r['is_latest'] = ret['is_latest']
            r['latest_object'] = ret['object']
            r['versions'] = ret['versions']
            if 'revoked' in ret['object']:
                r['revoked'] = ret['object']['revoked']
        r['source'] = str(self._source)
        r['target'] = str(self._target)
        r['caption'] = str(self._caption)
        r['type'] = str(self._type)
        return r


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
    _revoked = False
    _is_modified = False

    def __init__(self, id_, type_, caption, description, object_=None, observable_=None, cluster=None):
        super(AlchemyNode, self).__init__()
        self._id_ = id_
        self._set_type(type_)
        self._set_caption(caption)
        if(description is None):
            self._description = ''
        else:
            v = ''
            if isinstance(description, str):
                v = description
            elif isinstance(description, StructuredText):
                v = description.value

            if len(v) == 0:
                self._description = ''
            else:
                self._description = v
        self._cluster = cluster

    def __eq__(self, obj):
        return obj._id_ == self._id_

    def _set_caption(self, d):
        if(d is None):
            self._caption = ''
        else:
            self._caption = d

    def _set_type(self, d):
        self._type = d

    def set_cluster(self, cluster):
        self._cluster = cluster

    def set_is_exact(self, is_exact):
        self._is_exact = is_exact

    def get_id(self):
        return self._id_

    def set_value(self, value):
        self._value = value

    def get_json(self, ctirs):
        r = {}
        r['id'] = self.sanitize(str(self._id_))
        r['type'] = self.sanitize(str(self._type))
        r['caption'] = self.sanitize(self._caption)
        description = self.sanitize(self._description)
        r['stix2_object'] = self._stix2_object
        r['language_contents'] = self._language_contents
        r['user_language'] = self._user_language
        r['description'] = self.sanitize(description)
        r['cluster'] = self.sanitize(str(self._cluster))
        r['value'] = self.sanitize(self._value)
        r['revoked'] = False
        r['is_latest'] = False
        if self._stix2_object is not None:
            if 'modified' in self._stix2_object:
                ret = ctirs.get_latest_object(
                    self._stix2_object['id'],
                    self._stix2_object['modified'])
                r['modified'] = self._stix2_object['modified']
                r['is_latest'] = ret['is_latest']
                r['latest_object'] = ret['object']
                r['versions'] = ret['versions']
                if 'revoked' in ret['object']:
                    r['revoked'] = ret['object']['revoked']
        return r

    def sanitize(self, s):
        return s

    def set_language_contents(self, language_contents):
        self._language_contents = language_contents

    def set_stix2_object(self, _stix2_object):
        self._stix2_object = _stix2_object

    def set_user_language(self, _user_language):
        self._user_language = _user_language

    class RelatedCampaign:
        _campaign = ''
        _related_num = -1

        def __init__(self, campaign, related_num):
            self._campaign = campaign
            self._related_num = related_num
