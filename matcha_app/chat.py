from profile_db import *
from dict_ops import *
import time


def get_now_time():
    epoch_now = time.time()
    structtime_now = time.localtime(epoch_now)
    format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
    return format_now


def send_msg(email, to_email, msg):
    prof_dict = fetch_profiles({'email': email})[0]
    msgs = dict_val_similar_key(prof_dict, 'msgs')
    now_time = get_now_time()
    msgs.append({'date': now_time, 'to': to_email, 'msg': msg})
    update_profile(email, {'msgs': msgs})

