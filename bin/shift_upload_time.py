#!/usr/bin/python


import os
import django

if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctim.settings")
    django.setup()
    '''
    from util.demo import update_ctim_files,print_ctim_files_upload_time,get_shift_upload_time_delta
    
    #差分取得
    delta = get_shift_upload_time_delta()
    print 'shift delta:' + str(delta)
    
    #変更前表示
    print '----'
    print 'before'
    print '----'
    print_ctim_files_upload_time()
    print '----'

    #upload_time更新
    update_ctim_files(delta)

    #変更後表示
    print 'after'
    print '----'
    print_ctim_files_upload_time()
    print '----'

    '''