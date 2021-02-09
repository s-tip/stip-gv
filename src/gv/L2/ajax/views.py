import json
import re
import stix.extensions.marking.ais  # @UnusedImport
from stix.core.stix_package import STIXPackage
from cybox.objects.file_object import File
from cybox.objects.domain_name_object import DomainName
from cybox.objects.uri_object import URI
from cybox.objects.address_object import Address
from django.views.decorators.csrf import csrf_protect
from django.http.response import JsonResponse
from stip.common import get_text_field_value
from stip.common.label import sanitize_id
from stip.common.stix_customizer import StixCustomizer
from ctim.constant import SESSION_EXPIRY, DISPLAY_NODE_THRESHOLD
from core.api.rs import Ctirs
from core.alchemy.alchemy import AlchemyJsonData, AlchemyNode, AlchemyEdge

LABEL_EDGE = 'Includes'
LABEL_IDREF = 'IDref'
LABEL_UNSPECIFIED = 'Unspecified'
LABEL_V2_CREATED_BY_REF = 'created_by_ref'
LABEL_V2_OBJECT_REF = 'object_ref'
LABEL_V2_LABEL_REF = 'v2_label_ref'
LABEL_V2_CUSTOM_OBJECT_REF = 'v2_custom_object'
LABEL_V2_CUSTOM_PROPERTY_REF = 'custom_property_ref'


def get_l2_ajax_related_campagins_campaign(request):
    return get_text_field_value(request, 'campaign', default_value='')


def get_l2_ajax_related_campagins_similar_ip(request):
    return str2boolean(get_text_field_value(request, 'similar_ip', default_value=False))


def get_l2_ajax_related_campagins_similar_domain(request):
    return str2boolean(get_text_field_value(request, 'similar_domain', default_value=False))


def get_l2_ajax_related_campagins_i18n_info(request):
    return str2boolean(get_text_field_value(request, 'i18n', default_value=False))


def get_l2_ajax_related_campaign_nodes_base_campaign(request):
    return get_text_field_value(request, 'base_campaign', default_value='')


def get_l2_ajax_base_package(request):
    return get_text_field_value(request, 'base_package', default_value='')


def get_l2_ajax_too_many_nodes(request):
    return get_text_field_value(request, 'too_many_nodes', default_value='confirm')


def str2boolean(s):
    if s == "true":
        return True
    else:
        return False


def check_allow_l2_view(request):
    stip_user = request.user
    if not stip_user.is_active:
        r = {'status': 'NG',
             'message': 'You account is inactive.'}
        return JsonResponse(r, safe=False)
    return None


def related_packages(request):
    request.session.set_expiry(SESSION_EXPIRY)
    if request.method != 'GET':
        r = {'status': 'NG',
             'message': 'Invalid HTTP method'}
        return JsonResponse(r, safe=False)
    r = check_allow_l2_view(request)
    if r is not None:
        return r
    try:
        base_package = get_l2_ajax_base_package(request)
        is_ip_similar_check = get_l2_ajax_related_campagins_similar_ip(request)
        is_domain_similar_check = get_l2_ajax_related_campagins_similar_domain(request)
        exact = True
        ctirs = Ctirs(request)
        packages = ctirs.get_matched_packages(base_package, exact, is_ip_similar_check, is_domain_similar_check)
        return JsonResponse(packages, safe=False)
    except BaseException:
        import traceback
        traceback.print_exc()
        return JsonResponse(r, safe=False)


class TooMuchNodes(Exception):
    pass


@csrf_protect
def related_package_nodes(request):
    request.session.set_expiry(SESSION_EXPIRY)
    if request.method != 'POST':
        r = {'status': 'NG',
             'message': 'Invalid HTTP method'}
        return JsonResponse(r, safe=False)
    r = check_allow_l2_view(request)
    if r is not None:
        return r
    base_package = get_l2_ajax_base_package(request)
    compared_package_ids = request.POST.getlist('check_packages[]')
    is_ip_similar_check = get_l2_ajax_related_campagins_similar_ip(request)
    is_domain_similar_check = get_l2_ajax_related_campagins_similar_domain(request)
    i18n = get_l2_ajax_related_campagins_i18n_info(request)
    exact = True

    try:
        ctirs = Ctirs(request)
        ret = ctirs.get_contents_and_edges(base_package, exact, compared_package_ids, is_ip_similar_check, is_domain_similar_check)
        if ret is None:
            r = {'status': 'NG',
                 'message': ' /api/v1/gv/contents_and_edges has no data.'}
            return JsonResponse(r, safe=False)
    except BaseException:
        r = {'status': 'NG',
             'message': '/api/v1/gv/contents_and_edges error.'}
        return JsonResponse(r, safe=False)

    is_redact_confirm = get_l2_ajax_too_many_nodes(request)

    aj = AlchemyJsonData()
    for content in ret['contents']:
        try:
            set_alchemy_nodes(aj, content, is_redact_confirm)
        except TooMuchNodes:
            ret_json = {'status': 'WARNING',
                        'message': 'Too many nodes'}
            return JsonResponse(ret_json, safe=False)

    aj.set_json_node_user_language(request.user.language)

    if i18n:
        for object_ref, o_ in aj._json_nodes.items():
            if o_._stix2_object is None:
                continue
            modified = o_._stix2_object['modified']
            language_contents = ctirs.get_language_contents(object_ref, modified)
            if len(language_contents) > 0:
                modify_alchemy_node_language_content(aj, language_contents[0])

    for edge in ret['edges']:
        start_node_id = convert_valid_node_id(edge['start_node']['node_id'])
        end_node_id = convert_valid_node_id(edge['end_node']['node_id'])
        aj.set_json_node_exact(start_node_id)
        aj.set_json_node_exact(end_node_id)
        ae = AlchemyEdge(start_node_id, end_node_id, edge['edge_type'])
        aj.add_json_edge(ae)

    ret_json = aj.get_alchemy_json(is_redact_confirm)
    if ret_json is None:
        ret_json = {'status': 'WARNING',
                    'message': 'Too many nodes'}
        return JsonResponse(ret_json, safe=False)

    return JsonResponse(ret_json, safe=False)


def get_observable_value_string_from_list(list_):
    v_str = ''
    DELIIETER_STR = ',<br/>'
    for v in list_:
        v_str += ('%s%s' % (v, DELIIETER_STR))
    return v_str


def get_observable_value_string(observable):
    value_list, _ = get_observable_value(observable)
    return get_observable_value_string_from_list(value_list)


def get_v2_observable_value(observable):
    TYPE_V2_ETC_OBSERVABLE = 'v2_Etc_Observable'
    TYPE_V2_DOMAIN_NAME_OBSERVABLE = 'v2_domain_name_observable'
    TYPE_V2_IPV4_ADDR_OBSERVABLE = 'v2_ipv4_addr_observable'
    TYPE_V2_FILE_OBSERVABLE = 'v2_file_observable'
    TYPE_V2_WINDOWS_REGISTRY_KEY_OBSERVABLE = 'v2_Windows_Registry_Key_Observable'

    values = []
    if observable['type'] == 'ipv4-addr':
        value = observable['value']
        values.append(value)
        return values, value, value, TYPE_V2_IPV4_ADDR_OBSERVABLE
    elif observable['type'] == 'file':
        s = '<br/>\n'
        if 'name' in observable:
            values.append(observable['name'])
            s += ('Name: %s<br/>\n' % (observable['name']))
        if 'size' in observable:
            s += ('size: %d<br/>\n' % (observable['size']))
        if 'hashes' in observable:
            hashes = observable['hashes']
            if 'MD5' in hashes:
                values.append(hashes['MD5'])
                s += ('MD5: %s<br/>\n' % (hashes['MD5']))
            if 'SHA-1' in hashes:
                values.append(hashes['SHA-1'])
                s += ('SHA-1: %s<br/>\n' % (hashes['SHA-1']))
            if 'SHA-256' in hashes:
                values.append(hashes['SHA-256'])
                s += ('SHA-256: %s<br/>\n' % (hashes['SHA-256']))
            if 'SHA-512' in hashes:
                values.append(hashes['SHA-512'])
                s += ('SHA-512: %s<br/>\n' % (hashes['SHA-512']))
        return values, 'File', s, TYPE_V2_FILE_OBSERVABLE
    elif observable['type'] == 'windows-registry-key':
        value = observable['key']
        values.append(value)
        return values, value, value, TYPE_V2_WINDOWS_REGISTRY_KEY_OBSERVABLE
    elif observable['type'] == 'domain-name':
        value = observable['value']
        values.append(value)
        return values, value, value, TYPE_V2_DOMAIN_NAME_OBSERVABLE
    return values, observable['type'], str(str(observable)), TYPE_V2_ETC_OBSERVABLE


def get_observable_value(observable):
    value_list = []
    TYPE_ETC_OBSERVABLE = 'Etc_Observable'

    type_ = TYPE_ETC_OBSERVABLE

    object_ = observable.object_
    if object_ is None:
        return value_list, TYPE_ETC_OBSERVABLE

    prop = object_.properties

    if isinstance(prop, File):
        if prop.hashes is not None:
            for _hash in prop.hashes:
                if _hash.simple_hash_value is not None:
                    if _hash.simple_hash_value is not None:
                        value_list.append(_hash.simple_hash_value)
                        type_ = 'Observable_hash'
                if _hash.fuzzy_hash_value is not None:
                    if _hash.fuzzy_hash_value is not None:
                        value_list.append(_hash.fuzzy_hash_value)
                        type_ = 'Observable_hash'
        elif prop.file_name is not None:
            value_list.append(prop.file_name.value)
            type_ = 'Observable_file_name'
        else:
            print('no prop')
    elif isinstance(prop, DomainName):
        if prop.value is not None:
            if prop.value.value is not None:
                value_list.append(prop.value.value)
                type_ = 'Observable_domain'
    elif isinstance(prop, URI):
        if prop.value is not None:
            if prop.value.value is not None:
                value_list.append(prop.value.value)
                type_ = 'Observable_uri'
    elif isinstance(prop, Address):
        if prop.category == Address.CAT_IPV4:
            if prop.address_value is not None:
                value_list.append(prop.address_value)
                type_ = 'Observable_ip'
    else:
        print(type(prop))
    return value_list, type_


def set_alchemy_nodes(aj, content, too_many_nodes='confirm'):
    if content['version'].startswith('2.'):
        is_stix_v2 = True
    else:
        is_stix_v2 = False

    package_name = content['package_name']
    if is_stix_v2:
        if isinstance(content, dict):
            package = content['dict']
        else:
            package = json.loads(content['dict'])
    else:
        package = STIXPackage.from_dict(content['dict'])

    if is_stix_v2:
        stix_header = None
    else:
        stix_header = package.stix_header

    if is_stix_v2:
        an_package_id = package['id']
    else:
        an_package_id = convert_valid_node_id(package.id_)

    an_header_id = an_package_id

    if is_stix_v2:
        indicators = []
        observables = []
        campaigns = []
        threat_actors = []
        coas = []
        identies = []
        malwares = []
        sightings = []
        intrusion_sets = []
        attack_patterns = []
        relationships = []
        reports = []
        tools = []
        vulnerabilities = []
        custom_objects = []

        locations = []
        opinions = []
        notes = []
        language_contents = []
        groupings = []
        infrastructures = []
        malware_analysises = []
        '''
        x_stip_snses = []
        '''

        ttps = None
        ets = None
        incidents = None

        if len(package['objects']) > DISPLAY_NODE_THRESHOLD:
            if too_many_nodes == 'confirm':
                raise TooMuchNodes()

        for o_ in package['objects']:
            object_type = o_['type']
            if object_type == 'indicator':
                indicators.append(o_)
            elif object_type == 'identity':
                identies.append(o_)
            elif object_type == 'observed-data':
                observables.append(o_)
            elif object_type == 'malware':
                malwares.append(o_)
            elif object_type == 'sighting':
                sightings.append(o_)
            elif object_type == 'intrusion-set':
                intrusion_sets.append(o_)
            elif object_type == 'threat-actor':
                threat_actors.append(o_)
            elif object_type == 'attack-pattern':
                attack_patterns.append(o_)
            elif object_type == 'campaign':
                campaigns.append(o_)
            elif object_type == 'relationship':
                relationships.append(o_)
            elif object_type == 'course-of-action':
                coas.append(o_)
            elif object_type == 'report':
                reports.append(o_)
            elif object_type == 'tool':
                tools.append(o_)
            elif object_type == 'vulnerability':
                vulnerabilities.append(o_)
            elif object_type == 'location':
                locations.append(o_)
            elif object_type == 'opinion':
                opinions.append(o_)
            elif object_type == 'note':
                notes.append(o_)
            elif object_type == 'language-content':
                language_contents.append(o_)
            elif object_type == 'grouping':
                groupings.append(o_)
            elif object_type == 'infrastructure':
                infrastructures.append(o_)
            elif object_type == 'malware-analysis':
                malware_analysises.append(o_)
            elif object_type.startswith('x-'):
                if object_type == 'x-stip-sns':
                    continue
                else:
                    custom_objects.append(o_)
    else:
        indicators = package.indicators
        observables = package.observables
        campaigns = package.campaigns
        ttps = package.ttps
        threat_actors = package.threat_actors
        ets = package.exploit_targets
        coas = package.courses_of_action
        incidents = package.incidents

        identies = None
        malwares = None
        sightings = None
        intrusion_sets = None
        attack_patterns = None
        relationships = None
        reports = None
        tools = None
        vulnerabilities = None
        locations = None
        opinions = None
        notes = None
        language_contents = None
        custom_objects = None
        groupings = None
        infrastructures = None
        malware_analysises = None

    if not is_stix_v2:
        an = AlchemyNode(an_header_id, 'Header', package_name, stix_header.description, cluster=an_package_id)
        aj.add_json_node(an)

    if indicators is not None:
        if not is_stix_v2:
            an_indicators_id = an_package_id + '--indicators'
        else:
            an_indicators_id = None

        indicators_values = []
        for indicator in indicators:
            l = set_alchemy_node_indicator(aj, indicator, an_indicators_id, is_stix_v2, an_package_id)
            indicators_values.extend(l)

        if not is_stix_v2:
            an = AlchemyNode(an_indicators_id, 'Indicators', 'Indicators', '', cluster=an_package_id)
            an.set_value(get_observable_value_string_from_list(indicators_values))
            aj.add_json_node(an)
            ae = AlchemyEdge(an_header_id, an_indicators_id, LABEL_EDGE)
            aj.add_json_edge(ae)

    if observables is not None:
        if not is_stix_v2:
            an_observables_id = an_package_id + '--observables'
        else:
            an_observables_id = None
        obsevables_values = []
        for observed_data in observables:
            l = set_alchemy_node_observable(aj, observed_data, an_observables_id, is_stix_v2, an_package_id)
            obsevables_values.extend(l)

        if not is_stix_v2:
            an = AlchemyNode(an_observables_id, 'Observables', 'Observables', '', cluster=an_package_id)
            an.set_value(get_observable_value_string_from_list(obsevables_values))
            aj.add_json_node(an)
            ae = AlchemyEdge(an_header_id, an_observables_id, LABEL_EDGE)
            aj.add_json_edge(ae)

    if campaigns is not None:
        if not is_stix_v2:
            an_campaigns_id = an_package_id + '--campaigns'
            an = AlchemyNode(an_campaigns_id, 'Campaigns', 'Campaigns', '', cluster=an_package_id)
            aj.add_json_node(an)
            ae = AlchemyEdge(an_header_id, an_campaigns_id, LABEL_EDGE)
            aj.add_json_edge(ae)
        else:
            an_campaigns_id = None
        for campaign in campaigns:
            set_alchemy_node_campaign(aj, campaign, an_campaigns_id, is_stix_v2, an_package_id)

    if threat_actors is not None:
        if not is_stix_v2:
            an_tas_id = an_package_id + '--tas'
            an = AlchemyNode(an_tas_id, 'Threat_Actors', 'Threat_Actors', '', cluster=an_package_id)
            aj.add_json_node(an)
            ae = AlchemyEdge(an_header_id, an_tas_id, LABEL_EDGE)
            aj.add_json_edge(ae)
        else:
            an_tas_id = None
        for threat_actor in threat_actors:
            set_alchemy_node_threat_actor(aj, threat_actor, an_tas_id, is_stix_v2, an_package_id)

    if coas is not None:
        if not is_stix_v2:
            an_coas_id = an_package_id + '--coas'
            an = AlchemyNode(an_coas_id, 'Courses_Of_Action', 'Courses_Of_Action', '', cluster=an_package_id)
            aj.add_json_node(an)
            ae = AlchemyEdge(an_header_id, an_coas_id, LABEL_EDGE)
            aj.add_json_edge(ae)
        else:
            an_coas_id = None
        for coa in coas:
            set_alchemy_node_coa(aj, coa, an_coas_id, is_stix_v2, an_package_id)

    if ttps is not None:
        an_ttps_id = an_package_id + '--ttps'
        an = AlchemyNode(an_ttps_id, 'TTPs', 'TTPs', '', cluster=an_package_id)
        aj.add_json_node(an)
        ae = AlchemyEdge(an_header_id, an_ttps_id, LABEL_EDGE)
        aj.add_json_edge(ae)
        for ttp in ttps:
            set_alchemy_node_ttp(aj, ttp, an_ttps_id, an_package_id)

    if ets is not None:
        an_ets_id = an_package_id + '--ets'
        an = AlchemyNode(an_ets_id, 'Exploit_Targets', 'Exploit_Targets', '', cluster=an_package_id)
        aj.add_json_node(an)
        ae = AlchemyEdge(an_header_id, an_ets_id, LABEL_EDGE)
        aj.add_json_edge(ae)
        for et in ets:
            set_alchemy_node_et(aj, et, an_ets_id, an_package_id)

    if incidents is not None:
        an_incidents_id = an_package_id + '--incidents'
        an = AlchemyNode(an_incidents_id, 'Incidents', 'Incidents', '', cluster=an_package_id)
        aj.add_json_node(an)
        ae = AlchemyEdge(an_header_id, an_incidents_id, LABEL_EDGE)
        aj.add_json_edge(ae)
        for incident in incidents:
            set_alchemy_node_incident(aj, incident, an_incidents_id, an_package_id)

    if identies is not None:
        for identity in identies:
            set_alchemy_node_identity(aj, identity, an_package_id)

    if malwares is not None:
        for malware in malwares:
            set_alchemy_node_malware(aj, malware, an_package_id)

    if sightings is not None:
        for sighting in sightings:
            set_alchemy_node_sighting(aj, sighting, an_package_id)

    if intrusion_sets is not None:
        for intrusion_set in intrusion_sets:
            set_alchemy_node_intrusion_set(aj, intrusion_set, an_package_id)

    if attack_patterns is not None:
        for attack_pattern in attack_patterns:
            set_alchemy_node_attack_pattern(aj, attack_pattern, an_package_id)

    if reports is not None:
        for report in reports:
            set_alchemy_node_report(aj, report, an_package_id)

    if tools is not None:
        for tool in tools:
            set_alchemy_node_tool(aj, tool, an_package_id)

    if vulnerabilities is not None:
        for vulnerability in vulnerabilities:
            set_alchemy_node_vulnerability(aj, vulnerability, an_package_id)

    if locations is not None:
        for location in locations:
            set_alchemy_node_location(aj, location, an_package_id)

    if opinions is not None:
        for opinion in opinions:
            set_alchemy_node_opinion(aj, opinion, an_package_id)

    if notes is not None:
        for note in notes:
            set_alchemy_node_note(aj, note, an_package_id)

    if custom_objects is not None:
        for custom_object in custom_objects:
            set_alchemy_node_custom_object(aj, custom_object, an_package_id)

    if groupings is not None:
        for grouping in groupings:
            set_alchemy_node_grouping(aj, grouping, an_package_id)

    if infrastructures is not None:
        for infrastructure in infrastructures:
            set_alchemy_node_infrastructure(aj, infrastructure, an_package_id)

    if malware_analysises is not None:
        for malware_analysis in malware_analysises:
            set_alchemy_node_malware_analysis(aj, malware_analysis, an_package_id)

    '''
    if x_stip_snses is not None:
        for x_stip_sns in x_stip_snses:
            set_alchemy_node_x_stip_sns(aj, x_stip_sns, an_package_id)
    '''

    if relationships is not None:
        for relationship in relationships:
            set_alchemy_node_relationship(aj, relationship)
    return


def _set_label_alchemy_node(aj, object_, node_id, an_package_id):
    if 'labels' in object_:
        for label in object_['labels']:
            label_node_id = sanitize_id(label) + '--' + node_id
            an = AlchemyNode(label_node_id, 'v2_label', label, label, cluster=an_package_id)
            aj.add_json_node(an)
            ae = AlchemyEdge(node_id, label_node_id, LABEL_V2_LABEL_REF)
            aj.add_json_edge(ae)


def set_alchemy_node_campaign(aj, campaign, an_campaigns_id=None, is_stix_v2=False, an_package_id=None):
    if is_stix_v2:
        set_alchemy_node_campaign_v2(aj, campaign, an_package_id)
    else:
        set_alchemy_node_campaign_v1(aj, campaign, an_campaigns_id, an_package_id)


def set_alchemy_node_campaign_v2(aj, object_, an_package_id):
    an_campaign_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['aliases', 'first_seen', 'last_seen', 'objective']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(an_campaign_id, 'v2_campaign', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, an_campaign_id, an_package_id)
    return


def set_alchemy_node_campaign_v1(aj, campaign, an_campaigns_id, an_package_id):
    an_campaign_id = convert_valid_node_id(campaign.id_)
    an = AlchemyNode(an_campaign_id, 'Campaign', campaign.title, campaign.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_campaigns_id, an_campaign_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    if campaign.related_incidents is not None:
        for related_incident in campaign.related_incidents:
            relationship = related_incident.relationship if related_incident.relationship is not None else LABEL_UNSPECIFIED
            ae = AlchemyEdge(an_campaign_id, convert_valid_node_id(related_incident.item.idref), relationship)
            aj.add_json_edge(ae)
    if campaign.related_indicators is not None:
        for realated_indicator in campaign.related_indicators:
            relationship = realated_indicator.relationship if realated_indicator.relationship is not None else LABEL_UNSPECIFIED
            ae = AlchemyEdge(an_campaign_id, convert_valid_node_id(realated_indicator.item.idref), relationship)
            aj.add_json_edge(ae)
    if campaign.related_packages is not None:
        for related_package in campaign.related_packages:
            relationship = related_package.relationship if related_package.relationship is not None else LABEL_UNSPECIFIED
            ae = AlchemyEdge(an_campaign_id, convert_valid_node_id(related_package.item.idref), relationship)
            aj.add_json_edge(ae)
    if campaign.related_ttps is not None:
        for related_ttp in campaign.related_ttps:
            relationship = related_ttp.relationship if related_ttp.relationship is not None else LABEL_UNSPECIFIED
            ae = AlchemyEdge(an_campaign_id, convert_valid_node_id(related_ttp.item.idref), relationship)
            aj.add_json_edge(ae)
    if campaign.attribution is not None:
        for attribution in campaign.attribution:
            if attribution.threat_actor is not None:
                for threat_actor in attribution.threat_actor:
                    relationship = threat_actor.relationship if threat_actor.relationship is not None else LABEL_UNSPECIFIED
                    ae = AlchemyEdge(an_campaign_id, convert_valid_node_id(threat_actor.item.idref), relationship)
                    aj.add_json_edge(ae)
    return


ipv4_pattern = re.compile(r'ipv4-addr:value\s*=\s*\'(\S+)\'')
domain_name_pattern = re.compile(r'domain-name:value\s*=\s*\'(\S+)\'')
md5_pattern = re.compile(r'file:hashes\.\'MD5\'\s*=\s*\'(\S+)\'')
sha1_pattern = re.compile(r'file:hashes\.\'SHA-1\'\s*=\s*\'(\S+)\'')
sha256_pattern = re.compile(r'file:hashes\.\'SHA-256\'\s*=\s*\'(\S+)\'')
sha512_pattern = re.compile(r'file:hashes\.\'SHA-512\'\s*=\s*\'(\S+)\'')
url_pattern = re.compile(r'url:value\s*=\s*\'(\S+)\'')
email_addr_pattern = re.compile(r'email-addr:value\s*=\s*\'(\S+)\'')

patterns = [
    (ipv4_pattern, 'v2_ipv4_addr_observable'),
    (domain_name_pattern, 'v2_domain_name_observable'),
    (md5_pattern, 'v2_file_observable'),
    (sha1_pattern, 'v2_file_observable'),
    (sha256_pattern, 'v2_file_observable'),
    (sha512_pattern, 'v2_file_observable'),
    (url_pattern, 'v2_indicator'),
    (email_addr_pattern, 'v2_indicator'),
]


def _get_indicator_type_value_stix2(pattern_str):
    for pattern_tup in patterns:
        pattern, type_ = pattern_tup
        matches = pattern.findall(pattern_str)
        if len(matches) == 1:
            return type_, matches[0]
    return None, None


def set_alchemy_node_indicator(aj, indicator, an_indicators_id=None, is_stix_v2=False, an_package_id=None):
    indicators_values = []

    if is_stix_v2:
        an_indicator_id = convert_valid_node_id(indicator['id'])
        value_list = []
        type_ = 'v2_indicator'
    else:
        an_indicator_id = convert_valid_node_id(indicator.id_)
        if indicator.observable is not None:
            value_list, type_ = get_observable_value(indicator.observable)
        else:
            value_list = []
            type_ = ''

    indicators_values.extend(value_list)

    title, description = get_alchemy_indicator_title_description(indicator, is_stix_v2)
    an = AlchemyNode(an_indicator_id, type_, title, description, cluster=an_package_id)
    if is_stix_v2:
        an.set_stix2_object(indicator)

    if is_stix_v2:
        type_, value = _get_indicator_type_value_stix2(indicator['pattern'])
        if type_:
            an._set_type(type_)
            an._set_caption(value)
            an.set_value(value)
        else:
            an.set_value(indicator['pattern'])
    else:
        if indicator.observable is not None:
            an.set_value(get_observable_value_string(indicator.observable))
    aj.add_json_node(an)

    if is_stix_v2:
        set_created_by_ref_edge(aj, indicator)
        _set_label_alchemy_node(aj, indicator, an_indicator_id, an_package_id)
    else:
        ae = AlchemyEdge(an_indicators_id, an_indicator_id, LABEL_EDGE)
        aj.add_json_edge(ae)
        if indicator.observable is not None:
            if indicator.observable.idref is not None:
                ae = AlchemyEdge(an_indicator_id, convert_valid_node_id(indicator.observable.idref), LABEL_IDREF)
                aj.add_json_edge(ae)
        if indicator.indicated_ttps is not None:
            for ttp in indicator.indicated_ttps:
                ae = AlchemyEdge(an_indicator_id, convert_valid_node_id(ttp.item.idref), LABEL_IDREF)
                aj.add_json_edge(ae)
    return indicators_values


def get_alchemy_indicator_title_description_v1(indicator):
    title = None
    description = None

    if indicator.title is not None:
        title = indicator.title
    elif indicator.indicator_types is not None:
        if len(indicator.indicator_types) != 0:
            title = indicator.indicator_types[0].value

    if indicator.description is not None:
        description = indicator.description
    elif indicator.indicator_types is not None:
        if len(indicator.indicator_types) != 0:
            description = indicator.indicator_types[0].value
    return title, description


def get_alchemy_indicator_title_description_v2(object_):
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['labels', 'pattern', 'valid_from', 'valid_until', 'kill_chain_phases']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    return title, description


def get_alchemy_indicator_title_description(indicator, is_stix_v2=False):
    if is_stix_v2:
        return get_alchemy_indicator_title_description_v2(indicator)
    else:
        return get_alchemy_indicator_title_description_v1(indicator)


def set_alchemy_node_observable(aj, observed_data, an_observables_id=None, is_stix_v2=False, an_package_id=None):
    if is_stix_v2:
        obsevables_values = set_alchemy_node_observable_v2(aj, observed_data, an_package_id)
    else:
        obsevables_values = set_alchemy_node_observable_v1(aj, observed_data, an_observables_id, an_package_id)
    return obsevables_values


def set_alchemy_node_observable_v1(aj, observable, an_observables_id, an_package_id):
    node_id = convert_valid_node_id(observable.id_)
    value_list, type_ = get_observable_value(observable)
    title = ''
    if observable.title is not None:
        title = observable.title
    else:
        title = get_observable_value_string_from_list(value_list)
    an = AlchemyNode(node_id, type_, title, observable.description, cluster=an_package_id)
    an.set_value(get_observable_value_string(observable))
    aj.add_json_node(an)
    ae = AlchemyEdge(an_observables_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    return value_list


def set_alchemy_node_observable_v2(aj, object_, an_package_id):
    value_list = []
    node_id = convert_valid_node_id(object_['id'])
    for key, observable in object_['objects'].items():
        values, title, description, type_ = get_v2_observable_value(observable)
        value_list.extend(values)
        an_observable_id = '%s_%s' % (node_id, key)
        an = AlchemyNode(an_observable_id, type_, title, description, cluster=an_package_id)
        an.set_stix2_object(object_)
        aj.add_json_node(an)
        ae = AlchemyEdge(node_id, an_observable_id, LABEL_EDGE)
        aj.add_json_edge(ae)
    caption = node_id
    description = '<br/>\n'
    keys = ['first_observed', 'last_observed', 'number_observed']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    description += 'Values:<br/>\n'
    for v in value_list:
        description += ('%s<br/>\n' % (v))
    an = AlchemyNode(node_id, 'v2_observables-data', caption, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return value_list


def set_alchemy_node_threat_actor(aj, threat_actor, an_tas_id=None, is_stix_v2=False, an_package_id=None):
    if is_stix_v2:
        set_alchemy_node_threat_actor_v2(aj, threat_actor, an_package_id)
    else:
        set_alchemy_node_threat_actor_v1(aj, threat_actor, an_tas_id, an_package_id)
    return


def set_alchemy_node_threat_actor_v1(aj, threat_actor, an_tas_id, an_package_id):
    node_id = convert_valid_node_id(threat_actor.id_)
    an = AlchemyNode(node_id, 'Threat_Actor', threat_actor.title, threat_actor.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_tas_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    if threat_actor.observed_ttps:
        for observed_ttp in threat_actor.observed_ttps:
            relationship = observed_ttp.relationship if observed_ttp.relationship is not None else LABEL_UNSPECIFIED
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_ttp.item.idref), relationship)
            aj.add_json_edge(ae)


def set_alchemy_node_threat_actor_v2(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title='No title', default_description='No description')
    keys = ['aliases', 'roles', 'goals', 'sophistication', 'resource_level', 'primary_motivation', 'secondary_motivations']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_threat_actor', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_coa(aj, coa, an_coas_id, is_stix_v2, an_package_id):
    if is_stix_v2:
        set_alchemy_node_coa_v2(aj, coa, an_package_id)
    else:
        set_alchemy_node_coa_v1(aj, coa, an_coas_id, an_package_id)
    return


def set_alchemy_node_coa_v1(aj, coa, an_coas_id, an_package_id):
    node_id = convert_valid_node_id(coa.id_)
    an = AlchemyNode(node_id, 'Course_Of_Action', coa.title, coa.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_coas_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    return


def set_alchemy_node_coa_v2(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title='No title', default_description='No description')
    keys = ['action']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_coa', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    return


def set_alchemy_node_ttp(aj, ttp, an_ttps_id, an_package_id):
    node_id = convert_valid_node_id(ttp.id_)
    an = AlchemyNode(node_id, 'TTP', ttp.title, ttp.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_ttps_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, ttp, node_id, an_package_id)
    return


def set_alchemy_node_et(aj, et, an_ets_id, an_package_id):
    node_id = convert_valid_node_id(et.id_)
    an = AlchemyNode(node_id, 'Exploit_Target', et.title, et.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_ets_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, et, node_id, an_package_id)
    return


def set_alchemy_node_incident(aj, incident, an_incidents_id, an_package_id):
    node_id = convert_valid_node_id(incident.id_)
    an = AlchemyNode(node_id, 'Incident', incident.title, incident.description, cluster=an_package_id)
    aj.add_json_node(an)
    ae = AlchemyEdge(an_incidents_id, node_id, LABEL_EDGE)
    aj.add_json_edge(ae)
    return


def set_alchemy_node_identity(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title='No title', default_description='No description')
    keys = ['labels', 'identity_class', 'sectors', 'contact_information']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_identity', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_malware(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['labels', 'kill_chain_phases']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_malware', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_sighting(aj, object_, an_package_id):
    LABEL_V2_WHERE_SIGHTED_REF = 'v2_where_sighted_ref'
    LABEL_V2_OBSERVED_DATA_REF = 'v2_observed_data_ref'

    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description='')
    keys = ['first_seen', 'last_seen', 'count', 'summary']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_sighting', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'where_sighted_refs' in object_:
        for where_sighted_ref in object_['where_sighted_refs']:
            ae = AlchemyEdge(convert_valid_node_id(where_sighted_ref), node_id, LABEL_V2_WHERE_SIGHTED_REF)
            aj.add_json_edge(ae)
    if 'observed_data_refs' in object_:
        for observed_data_ref in object_['observed_data_refs']:
            ae = AlchemyEdge(convert_valid_node_id(observed_data_ref), node_id, LABEL_V2_OBSERVED_DATA_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_intrusion_set(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['aliases', 'first_seen', 'last_seen', 'goals', 'resource_level', 'primary_motivation', 'secondary_motivations']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_intrusion_set', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_attack_pattern(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['external_references', 'kill_chain_phases']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_attack_pattern', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_report(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['labels', 'published']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_report', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_tool(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['labels', 'kill_chain_phases', 'tool_version']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_tool', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_vulnerability(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['external_references']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_vulerability', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    index = 1
    if 'external_references' in object_:
        for external_reference in object_['external_references']:
            if 'source_name' in external_reference:
                if external_reference['source_name'] == 'cve':
                    if 'external_id' in external_reference:
                        cve = external_reference['external_id']
                        cve_node_id = convert_valid_node_id('%s-%s' % (node_id, cve))
                        cve_an = AlchemyNode(cve_node_id, 'v2_cve', cve, cve, cluster=an_package_id)
                        aj.add_json_node(cve_an)
                        index += 1
                        cve_ae = AlchemyEdge(cve_node_id, node_id, LABEL_V2_OBJECT_REF)
                        aj.add_json_edge(cve_ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_location(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['latitude', 'longitude', 'precision', 'region', 'country', 'administrative_area', 'city', 'code', 'postal_code']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_location', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_opinion(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['explanation', 'authors', 'opinion']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_opinion', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_note(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['abstract', 'content', 'authors']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_note', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_grouping(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['context']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_grouping', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_infrastructure(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['infrastructure_types', 'aliases', 'kill_chain_phases', 'first_seen', 'last_seen']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_infrastructure', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_malware_analysis(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    keys = ['product', 'version', 'host_vm_ref', 'operating_system_ref', 'installed_software_refs',
        'configuration_version', 'modules', 'analysis_engine_version', 'analysis_definition_version',
        'submitted', 'analysis_started', 'analysis_ended', 'result_name', 'result',
        'analysis_sco_refs', 'sample_ref']
    for key in keys:
        if key in object_:
            description += get_description_string_from_attr(object_, key)
    an = AlchemyNode(node_id, 'v2_malware_analysis', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return


def set_alchemy_node_custom_object(aj, object_, an_package_id):
    return _set_alchemy_node_custom_object(aj, object_, an_package_id)


def _set_alchemy_node_custom_object(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    node_type = 'v2_CustomObject_' + object_['type']
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    an = AlchemyNode(node_id, node_type, title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
    _set_label_alchemy_node(aj, object_, node_id, an_package_id)
    return

    stix_customizer = StixCustomizer.get_instance()
    if object_['type'] not in stix_customizer.get_custom_object_list():
        custom_properties_list = []
    else:
        custom_properties_list = stix_customizer.get_custom_object_dict()[object_['type']]

    for prop in object_:
        if prop not in custom_properties_list:
            continue
        prop_node_id = '%s-%s' % (node_id, prop)
        an = AlchemyNode(prop_node_id, 'v2_CustomObject', object_[prop], object_[prop], cluster=an_package_id)
        an.set_stix2_object(object_)
        aj.add_json_node(an)
        ae = AlchemyEdge(convert_valid_node_id(node_id), prop_node_id, LABEL_V2_CUSTOM_PROPERTY_REF)
        aj.add_json_edge(ae)
    return



'''
def set_alchemy_node_x_stip_sns(aj, object_, an_package_id):
    node_id = convert_valid_node_id(object_['id'])
    title, description = get_common_title_description(object_, default_title=object_['id'], default_description=object_['id'])
    an = AlchemyNode(node_id, 'v2_x_stip_sns', title, description, cluster=an_package_id)
    an.set_stix2_object(object_)
    aj.add_json_node(an)
    set_created_by_ref_edge(aj, object_)
    if 'object_refs' in object_:
        for observed_data_ref in object_['object_refs']:
            ae = AlchemyEdge(node_id, convert_valid_node_id(observed_data_ref), LABEL_V2_OBJECT_REF)
            aj.add_json_edge(ae)
'''


def modify_alchemy_node_language_content(aj, object_):
    ref_id = object_['object_ref']
    language_contents = object_['contents']

    ref_aj = aj.get_alchemy_node_by_id(ref_id)
    ref_aj.set_language_contents(language_contents)
    return


def set_alchemy_node_relationship(aj, object_):
    source_ref = object_['source_ref']
    target_ref = object_['target_ref']
    relationship_type = object_['relationship_type']
    ae = AlchemyEdge(source_ref, target_ref, relationship_type, LABEL_V2_CUSTOM_OBJECT_REF)
    aj.add_json_edge(ae)
    return


def get_common_title_description(object_, default_title=None, default_description=None):
    title = ''
    description = ''
    if 'name' in object_:
        title = object_['name']
    else:
        title = default_title
    if 'description' in object_:
        description = object_['description']
    else:
        description = default_description
    description += '<br/>\n'
    return title, description


def get_description_string_from_attr(dict_, key_, title=None):
    s = ''
    if title is None:
        s += ('%s: ' % (key_))
    else:
        s += ('%s: ' % (title))
    v = dict_[key_]
    if isinstance(v, list):
        for label in v:
            if isinstance(label, str):
                s += str(label) + ', '
            elif isinstance(label, dict):
                s += str(label) + ', '
            else:
                s += label + ', '
    elif isinstance(v, str):
        s += str(v)
    elif isinstance(v, str):
        s += v
    elif isinstance(v, int):
        s += str(v)
    if s.endswith(', '):
        s = s[:-2]
    s += '<br/>\n'
    return s


def set_created_by_ref_edge(aj, dict_):
    if 'created_by_ref' in dict_:
        ae = AlchemyEdge(convert_valid_node_id(dict_['created_by_ref']), convert_valid_node_id(dict_['id']), LABEL_V2_CREATED_BY_REF)
        aj.add_json_edge(ae)
    return


def _set_created_by_ref_edge_stip_custom_object(aj, dict_):
    if 'created_by_ref' in dict_:
        ae = AlchemyEdge(convert_valid_node_id(dict_['created_by_ref']), convert_valid_node_id(dict_['id']), LABEL_V2_CREATED_BY_REF)
        aj.add_json_edge(ae)
    return


def convert_valid_node_id(id_):
    return id_.replace(':', '--')
