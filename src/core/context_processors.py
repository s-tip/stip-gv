
from django.conf import settings as django_settings

#Header に埋め込む動的情報
def headers(request):
    d = {}
    #GitVersion
    d['git_version'] = django_settings.STIP_GV_VERSION
    return d