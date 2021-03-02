#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/02/25
# file: comparison.py
# Email:
# Author: 唐政 

def push_wechat_custom_msg(open_ids, src_name, url, msg_title, title, msg, event_time):
    """
    自定义消息推送
    """
    # noinspection PyBroadException
    try:
        if isinstance(event_time, datetime.datetime):
            event_time = event_time.strftime(BASE_DATETIME_FORMAT)
        elif isinstance(event_time, str):
            pass
        elif not event_time:
            event_time = timezone.now().strftime(BASE_DATETIME_FORMAT)
        data = {
            "first": {"value": title, },
            'keyword1': {"value": src_name},
            'keyword2': {"value": event_time},
            'remark': {"value": msg}
        }
        if msg_title:
            data['keyword3'] = {"value": msg_title, 'color': '#ff0000'}
        _thread.start_new_thread(push_wechat_msg_sendtry, (10, url, open_ids, data))
    except Exception as e:
        send_sentry(e)