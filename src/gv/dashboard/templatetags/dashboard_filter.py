# -*- coding: utf-8 -*-
from django import template
from django.utils import dateformat

register = template.Library()
@register.filter(name='get_dashboard_latest_cti_timestamp_format')
#dashboardのLatest CTIテーブルのTimestamp(datetime型)の表示フィルター
def get_dashboard_latest_cti_timestamp_format(timestamp):
    return dateformat.format(timestamp,'Y/m/d h:i:s')
