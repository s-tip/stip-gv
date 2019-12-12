#!/usr/bin/python3
##############################
# ctim_gv_regist.py
# CTIM GraphView bulk upload
##############################
# 第1引数：STIXdir
# 第2引数：uploader name
# 第3引数：vendor source
##############################

import argparse
import glob
import os
import traceback

from django.core.wsgi import get_wsgi_application

########
# main #
########
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctim.settings')
    application = get_wsgi_application()

    '''
    from core.neo4j.neo4j_upload import StixFileUpload
    from ctim.models import GVAuthUser,INPUT_SOURCE_SCRIPT
    from gv.sharing.ajax.views import get_campaign_no_specify_campaign

    parser = argparse.ArgumentParser(description = 'CTIM GraphView bulk upload')
    parser.add_argument('stix_dir',help='STIX_DIR_PATH')
    parser.add_argument('uploader',help='Uploder name')
    parser.add_argument('vendor_source',help='Vendor source name')
    args = parser.parse_args()

    try:
        try:
            uploader = GVAuthUser.objects.get(username=args.uploader)
        except Exception as e:
            print 'Invalid uploader(%s).' % (args.uploader)
            raise(e)
        upload = StixFileUpload(user=uploader)
        for stix_file_path in glob.glob('%s/*.xml' % (args.stix_dir)):
            with open(stix_file_path,'r', encoding='utf-8') as fp:
                campaign_name = get_campaign_no_specify_campaign(fp.read(),args.vendor_source)
            upload.upload(stix_file_path,campaign_name,args.vendor_source,input_source=INPUT_SOURCE_SCRIPT)
        ret = 0
    except Exception as e:
        print traceback.format_exc()
        print e.message
        ret = 1
    '''

    exit(ret)
