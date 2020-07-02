import json
from ctirs.models import Config


# SharingPolicyのModelの接尾辞
MODEL_SUFFIX = '-model'


# SharingPolicyの見出しの文字列を取得
def get_policy_communities():
    comms_list = []
    _conf_file_path = Config.objects.get_config().path_sharing_policy_specifications
    try:
        with open(_conf_file_path, 'r', encoding='utf-8') as fp:
            df = json.load(fp)
            roots = df.get("ROOT", [])
            for root in roots:
                policyset = root.get("PolicySet", [])
                for policy in policyset:
                    refs = policy.get("ref", [])
                    for ref in refs:
                        metatype = ref.get("Metatype")
                        if metatype == "SharingCommunityRef":
                            val = ref.get("Attributes", {}).get("name", None)
                            if val is not None:
                                comms_list.append(val)
        # 順序を保持して重複除去
        comms_list = sorted(set(comms_list), key=comms_list.index)
        # カンマ区切りの文字列に変換
        comms = ','.join(comms_list)
        return comms
    except Exception as e:
        print(e)
    return ''


# /**
# * Gets redaction policy.
# */
def get_policy(arg_community):
    arg_community = str(arg_community)
    try:
        rule_list = []
        _conf_file_path = Config.objects.get_config().path_sharing_policy_specifications
        with open(_conf_file_path, 'r', encoding='utf-8') as fp:
            df = json.load(fp)
            roots = df.get("ROOT", [])
            for root in roots:
                policyset = root.get("PolicySet", [])
                for policy in policyset:
                    refs = policy.get("ref", [])
                    flg_community = False
                    read_rule = []
                    for ref in refs:
                        metatype = ref.get("Metatype")
                        if metatype == "SharingCommunityRef":
                            val = ref.get("Attributes", {}).get("name", None)
                            if val == arg_community:
                                flg_community = True
                        if metatype == "Rule":
                            read_rule.extend(ref.get("ref", []))
                    if flg_community:
                        rule_list.extend(read_rule)

        rules = []
        for rule in rule_list:
            elems = []
            color = '#123456'
            redacts = []
            targets = rule.get("ref", [])
            for target in targets:
                metatype = target.get("Metatype")
                if metatype == "Action":
                    redacts.extend(target.get("Attributes", {}).get("regular_expression", []))

                if metatype.endswith(MODEL_SUFFIX):
                    elems.append(metatype[:-len(MODEL_SUFFIX)])

            for elem in elems:
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
