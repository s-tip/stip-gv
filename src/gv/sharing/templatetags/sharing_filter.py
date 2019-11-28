
from django import template

register = template.Library()
@register.filter(name='get_community_check_status')
#sharing.communityのcheckboxのstatusを返却
def get_community_check_status(community_info,community):
    if community in community_info:
        return 'checked' if community_info[community] == True else ''
    else:
        return ''
