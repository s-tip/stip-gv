
'''
import datetime
from django.utils.timezone import utc
from ctim.models import Files

def get_latest_upload_time():
    return Files.objects.all().order_by('upload_time').reverse()[0].upload_time

def get_shift_upload_time_delta():
    #現在時刻
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    #差分
    return now - get_latest_upload_time()

def update_ctim_files(delta):
    #Filesに対してすべてupload_timeをdelta分シフトする
    for file_ in Files.objects.all():
        file_.upload_time += delta
        file_.save()

def print_ctim_files_upload_time():
    for file_ in Files.objects.all().order_by('upload_time').reverse():
        print '%s:%s' % (file_.campaign_name,file_.upload_time)
    return

def shift_ctim_files_upload_time():
    #差分
    delta = get_shift_upload_time_delta()
    #Filesに対してすべてupload_timeをdelta分シフトして保存する
    update_ctim_files(delta)
'''
