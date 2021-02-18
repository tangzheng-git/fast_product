from production_manage.models import ProductionRecordItem, ProductionRecord
from django.db.models import Q
from liyuoa.liyuoa_tools import get_db_data_key_value_by_flag

now = datetime.datetime.now() - datetime.timedelta(hours=10)

fields = ["id", "plan_item__roll_no", "plan_item__num", "plan_item__weight", "plan_item__prod_thick"]
l = [x for x in ProductionRecord.objects.filter(org_id=ORG_ID, is_active=True,
                                                create_time__gt=now).order_by("-sort", "-id").values(*fields)[:1]]
log_append(1, "check", "roll_no", l)
if l:
    pr_record = l[0]
    record_id = pr_record.get("id")
    plan_item__roll_no = pr_record.get("plan_item__roll_no")
    plan_item__num = pr_record.get("plan_item__num")
    plan_item__weight = pr_record.get("plan_item__weight")
    plan_item__prod_thick = pr_record.get("plan_item__prod_thick")
    plan_item_single_weight = plan_item__weight / plan_item__num
    alarm = None
    key_list = result.keys()
    cache_warn = ""

    warn_list = get_db_data_key_value_by_flag("zha_gang_fu_cha_target_%s_%s" % (plan_item__prod_thick, ORG_ID))
    log_append("resultdata", "func", "123", warn_list)
    if not warn_list:
        save_result_msg("请设置该口径警报值")
        return

    for each_key in key_list:
        start_key = each_key.split("#")[0]
        log_append("start", "key", "roll_no", [start_key, plan_item__roll_no])
        if start_key != str(plan_item__roll_no):
            if "shibai" not in each_key:
                result.pop(each_key)
            else:
                cache_warn += result.pop(each_key)

    recorditem_query = ProductionRecordItem.objects.values("weight", "real_weight", "production_record_id", "id",
                                                           "index").using(ORG_ID).filter(org_id=ORG_ID, is_active=True,
                                                                                         production_record_id=record_id).order_by(
        "sort")
    log_append("record", "query", "list", list(recorditem_query))
    warning_txt = ""
    if not recorditem_query.exists():
        log_append(0, "check", "roll_no", "无轧制")
        before_txt = ""
    else:
        before_txt = "轧制序号%s" % plan_item__roll_no
        alarm_index_list = []
        for each_item in recorditem_query:
            weight = each_item.get("weight")
            real_weight = each_item.get("real_weight")
            index = each_item.get("index")
            cache_key = "%s#%s" % (str(plan_item__roll_no), index)

            if real_weight in [0, -1, None]:
                not_get_txt = "第%s支根支,实重获取失败," % index
                result[cache_key + "shibai"] = before_txt + not_get_txt
                continue
            else:
                try:
                    result.pop(cache_key + "shibai")
                except:
                    pass
            cha = real_weight - plan_item_single_weight
            if cha < warn_list["min_value"] or cha > warn_list["max_value"]:
                try:
                    bobao_num = result[cache_key]
                except:
                    bobao_num = 0
                if bobao_num >= 2:
                    continue
                warning_txt += "第%s支根支,实重与理重差值为%s,超出设定负差范围" % (index, cha)
                result[cache_key] = bobao_num + 1

    if warning_txt or cache_warn:
        PARMS = {"app_id": APPID, "app_key": APPKEY, "secret_key": SECRETKEY}
        if warning_txt:
            final_txt = cache_warn + before_txt + warning_txt
        else:
            final_txt = cache_warn
        parms = {"flag": MQTT_ROUTE, "name": name, "level": level, "message": final_txt}
        status, msg, datas = get_result_by_remote_consul_server(service_name='liyudas',
                                                                url='audio/api/create_audio_message',
                                                                json_parms=parms)
        if status == 0 and isinstance(datas, dict):
            if datas['success']:
                save_result_msg("生成音频消息成功")
            else:
                save_result_msg("生成音频消息失败")
        else:
            save_result_msg("调用微服务失败: %s" % status)
        parms = {}
        parms.update(PARMS)
        parms["txt"] = final_txt
        status, msg, datas = get_result_by_remote_consul_server(service_name='liyusf', url='static_file/api/set_auido',
                                                                json_parms=parms)

        if status == 0 and isinstance(datas, dict):
            if datas['success']:
                mp3_url = datas.get("result", {}).get("url", "")
                send_mqtt(route=MQTT_ROUTE,
                          msg={"url": mp3_url, "time": 1, "seconds": 12, "level": 3, "name": parms['txt'],
                               "display_name": parms['txt']})
                save_result_msg("生成音频成功")
            else:
                save_result_msg("生成音频失败")
        else:
            save_result_msg("调用微服务失败: %s" % status)



