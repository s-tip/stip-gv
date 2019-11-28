#!/usr/bin/python
# coding: UTF-8
##############################
#otx_downloader.py
#AlienVault OTX Downloader
##############################
#第1引数：key
#第2引数：download_dir
#第3引数：vendor source
##############################
import sys,traceback,argparse,os,glob,datetime,pytz
import traceback
from core.otx.vendor.OTXv2 import OTXv2
from core.otx.vendor.StixExport import StixExport 

########
# main #
########
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'AlienVault OTX Downloader')
    parser.add_argument('key',help='APIKEY')
    parser.add_argument('download_dir',help='download directory')
    parser.add_argument('-mt','--mtimestamp',help='Since datetime(%Y%m%d%H%M%S)',default=None)
    args = parser.parse_args()
 
    try:
        ret = 0
        #otxからmtimestamp以降のデータを取得する
        try:
            mtimestamp = datetime.datetime.strptime(args.mtimestamp,'%Y%m%d%H%M%S').replace(tzinfo=pytz.utc).isoformat()
        except:
            mtimestamp = None
        #otxから取得
        otx = OTXv2(args.key)
        count = 0
        for slice_ in otx.getsince(mtimestamp):
            #stix一つごとに登録処理
            stix = StixExport(slice_)
            stix.build()
            filename = '%04d.xml' % (count)
            filepath  = os.path.join(args.download_dir,filename)
            with open(filepath,'w') as fp:
                fp.write(stix.to_xml())
            count += 1
        n = datetime.datetime.now().replace(tzinfo=pytz.utc)
        print(n.strftime('%Y%m%d%H%M%S'))
    except Exception as e:
        print(traceback.format_exc())
        print(e.message)
        ret = 1

    exit(ret)
