
import re
from ctirs.models import Config

SHARING_COMMUNITY_PATTERN=re.compile('SHARING_COMMUNITY=\"(\\w+)\"')
STIX_ELEMENT_PATTERN = re.compile('STIX_ELEMENT=\"(\\w+)Model\"')
ACTION_PATTERN = re.compile('ACTION=\"(.*?)\\:USE_COLOR\\:(.*?)\"')
REDACTION_PATTERN = re.compile('REDACTION_FORMAT=\"(.*?)\"')

#SharingPolicyの見出しの文字列を取得
def get_policy_communities():
    comms = ''
    _conf_file_path = Config.objects.get_config().path_sharing_policy_specifications
    try:
        with open(_conf_file_path,'r') as fp:
            for line in fp:
                if((line is not None) and ('SHARING_COMMUNITY=' in line)):
                    for m in SHARING_COMMUNITY_PATTERN.finditer(line):
                        s = (m.group(1))
                        if((s in comms) == False):
                            comms += (s + ',')
        if(len(comms) == 0):
            return ''
        comms = comms[:-1] if comms[-1] == ',' else comms+'}'
        return comms
    except Exception as e:
        print(e)
    return ''

#/**
# * Gets redaction policy.
# */
def get_policy(arg_community):
    arg_community = str(arg_community)
    lines = []
    try:
        _conf_file_path = Config.objects.get_config().path_sharing_policy_specifications
        file_ = ''
        with open(_conf_file_path,'r') as fp:
            for line in fp:
                line = line.rstrip('\n')
                if((line != 'SHARING RULE SPECIFICATIONS') and (line != '***************************')):
                    file_ += (line + '\n')
                    lines.append(line)
        rules = []
        policies = file_.split('---POLICY_END---')

        for pol in policies:
            coms = []
            for m in SHARING_COMMUNITY_PATTERN.finditer(pol):
                coms.append(m.group(1))
            elems = []
            for m in STIX_ELEMENT_PATTERN.finditer(pol):
                elems.append(m.group(1))
            color = '#123456'
            for m in ACTION_PATTERN.finditer(pol):
                color = m.group(2)
            redacts = []
            for m in REDACTION_PATTERN.finditer(pol):
                redacts.append(m.group(1))
            for com in coms:
                for elem in elems:
                    if(com.upper().count(arg_community.upper()) > 0):
                        for redact in redacts:
                            d = {}
                            d['community'] = arg_community
                            d['type'] = elem
                            d['color'] = color
                            d['reg_exp'] = redact
                            rules.append(d)
        return rules
    except Exception as e:
        print(e)
        return None
