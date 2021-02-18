from util.script_api import get_result_by_remote_consul_server, log_append

import json


def query_menu_list_api():
    error_str = None
    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="jyx_kpi",
            url="permission/api/query_all_menu_list_api",
            data_parms={},
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"菜单数据查询:query_all_menu_list_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def query_api_url_list_api():
    error_str = None
    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="jyx_kpi",
            url="permission/api/query_api_url_list_api",
            data_parms={},
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"接口数据查询:query_api_url_list_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def auto_create_apiurl_api():
    error_str = None
    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="jyx_kpi",
            url="permission/api/auto_create_apiurl_api",
            data_parms={},
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"同步接口数据:auto_create_apiurl_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def get_menu_state_info_api(menu_id):
    error_str = None
    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="jyx_kpi",
            url="permission/api/get_menu_state_info_api",
            data_parms={
                'menu_id': menu_id,
            },
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"获取菜单对应的json:get_menu_state_info_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def query_file_list_api(name_start, name_end=None):
    error_str = None
    data_params = {
        'name_start': name_start
    }
    if name_end:
        data_params['name_end'] = name_end

    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="liyusf",
            url="static_file/api/query_static_file_by_name_list_api",
            data_parms=data_params,
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"静态文件查询:query_file_list_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def update_menu_api(menu_id, state_api_json):
    error_str = None
    data_params = {
        'menu_id': menu_id,
        'state_api_json': state_api_json,
    }
    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="jyx_kpi",
            url="permission/api/update_menu_api",
            data_parms=data_params,
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"菜单数据更新:update_menu_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


def deal_app_package_list():
    pass


def get_controller_api_dict(file_list):
    controller_dict = {}

    for js_file in file_list:
        content_list = js_file['content'].split('\n')
        _dict = {}
        result_controller = None
        for line in content_list:
            # 过滤注释行
            if line.strip()[0:2] == '//':
                continue

            import re
            pattern_controller = re.compile(r"app\.controller\([\"\'](.*?)[\'\"]")
            pattern_api = re.compile(r"api\.(.*?)\.(.*?)\(")
            pattern_modal_box = re.compile(r"modalBox\.show\([\"\'](.*?)[\'\"]")

            line_controller = pattern_controller.findall(line)
            result_api = pattern_api.findall(line)
            result_modal_box = pattern_modal_box.findall(line)

            if line_controller:
                # [("line_controller")]
                result_controller = line_controller[0]
                _js_file = {'js_file': js_file['name']}
                _dict.setdefault(result_controller, {}).update(_js_file)

            if result_controller and result_api:
                full_dir = '{}/{}'.format(result_api[0][0].strip(), result_api[0][1].strip())
                _dict[result_controller].setdefault('local_api', set()).add(full_dir)

            if result_controller and result_modal_box:
                _dict[result_controller].setdefault('modal_box_main', set()).add(result_modal_box[0])

        if _dict.get('local_api', None):
            _dict[result_controller]['local_api'] = list(_dict['local_api'])
        if _dict.get('modal_box_main', None):
            _dict[result_controller]['modal_box_main'] = list(_dict['modal_box_main'])

        controller_dict.update(_dict)
    return controller_dict


def deal_controller_api_package(package_list, controller_dict, api_list):
    control_api_list = []
    for controller in controller_dict.keys():
        _dict = {}
        # 数据处理
        for app in package_list:
            if app.get('controller', None) and app['controller'] == controller:
                _dict = {
                    "state_name": app['state_name'] if app.get('state_name', None) else None,
                    "controller": app['controller'],
                    "js_file": controller_dict[controller]['js_file'],
                }
                # 控制下url 检查数据库
                if controller_dict[controller].get('local_api', None):

                    _dict['local_api'] = []
                    for api_in_local in controller_dict[controller]['local_api']:

                        api_id = ''
                        api_name = ''
                        api_auth = False
                        state = -2

                        # if 'set_revise_number' in api_in_local:
                        #     print(_dict['js_file'])

                        for api_in_sql in api_list:
                            if api_in_sql['url'] == api_in_local:
                                state = -1
                                api_id = api_in_sql['id']
                                api_name = api_in_sql['name']
                                api_auth = api_in_sql['is_auth']
                                break

                        _dict['local_api'].append(
                            {
                                'id': api_id,
                                'name': api_name,
                                'url': api_in_local,
                                'is_auth': api_auth,
                                'state': state
                            }
                        )
                break

        if _dict:
            control_api_list.append(_dict)

    return control_api_list


def deal_control_api_modal_box(control_api_list, package_list):
    # 模态框处理
    for control_api in control_api_list:
        if control_api.get('modal_box_main', None):
            control_api['modal_box_controller'] = []
            for box_main in control_api['modal_box_main']:
                for app in package_list:
                    if app.get('main', None) and app['main'] == box_main:
                        control_api['modal_box_controller'].append(app['controller'])

    # 模态框api
    for control_api in control_api_list:
        if control_api.get('modal_box_controller', None):
            for box_controller in control_api['modal_box_controller']:
                for control in control_api_list:
                    if box_controller == control['controller']:
                        control_api['box_url'] = control.get('local_api', None)
    return control_api_list


def deal_contrast_result_dict(menu_list, control_api_list):
    for menu_item in menu_list:

        for control_api in control_api_list:
            if control_api['state_name'] == menu_item['state']:

                if control_api.get('local_api', None):

                    url_list = []
                    for far_end_url in menu_item['url_id_list']:
                        url_list.append(far_end_url['url'])

                    for item in control_api['local_api']:
                        if item['state'] == -1:
                            if item['url'] in url_list:
                                item['state'] = 1
                            else:
                                item['state'] = 0
                    # # 处理源数据 打印
                    new_api_list = control_api['local_api']
                    # for item in new_api_list:
                    #     print('菜单id', menu_item['id'])
                    #     print('菜单名称', menu_item['name'])
                    #     print('id', item.get('id', None))
                    #     print('name', item.get('name', None))
                    #     print('is_auth', item.get('is_auth', None))
                    #     print('url', item.get('url', None))
                    #     print('state', item.get('state', None))
                    #     print()

                    # 数据库源数据 打印
                    old_, old_error = get_menu_state_info_api(menu_item['id'])
                    if old_ and old_.get('state_api_json', None):
                        old_api_list = json.loads(old_['state_api_json'])
                        old_api_url_list = [_item['url'] for _item in old_api_list]
                        # for api in old_api_list:
                        #     print('菜单id', menu_item['id'])
                        #     print('菜单名称', menu_item['name'])
                        #     print('id', api.get('id', None))
                        #     print('name', api.get('name', None))
                        #     print('is_auth', api.get('is_auth', None))
                        #     print('url', api.get('url', None))
                        #     print('state', api.get('state', None))
                        # print()
                    else:
                        old_api_list = []
                        old_api_url_list = []

                    for new_api in new_api_list:
                        if new_api['url'] not in old_api_url_list:
                            # js文件新增url 添加进去
                            old_api_list.append(new_api)
                        else:
                            # 同步状态
                            for old_api in old_api_list:
                                if new_api['url'] == old_api['url']:
                                    old_api['is_auth'] = new_api['is_auth']
                                    old_api['state'] = new_api['state']
                                    break

                    for api in old_api_list:
                        print('菜单id', menu_item['id'])
                        print('菜单名称', menu_item['name'])
                        print('id', api.get('id', None))
                        print('name', api.get('name', None))
                        print('is_auth', api.get('is_auth', None))
                        print('url', api.get('url', None))
                        print('state', api.get('state', None))
                    print()

                    # 新数据处理以便于上传
                    jso = json.dumps(old_api_list)

                    # 同步数据库
                    update_menu_api(menu_item['id'], jso)
                    break
        else:
            pass


app_package_start = 'pc/www/base/app_package.json'
app_package_json_list = []
app_package_json_dict = {}
app_package_json = []
# 获取线上app_package 文件 1.0
app_package_result, app_package_error = query_file_list_api(app_package_start)
if app_package_result:
    # app_package_json_list = [
    #     {
    #         'id': '',
    #         'name': '',
    #         'content': '',
    #     },
    # ]
    app_package_json_list = app_package_result['list']
    if app_package_json_list:
        app_package_json_dict = app_package_json_list[0]
        app_package_json = app_package_json_dict['content']
        # app_package_json = [
        #     {
        #
        #     },
        # ]
        app_package_json = json.loads(app_package_json)


js_file_start = 'pc/www/app'
js_file_end = 'js'
js_file_list = []
controller_api_dict = {}
# 获取线上 控制器 api信息 1.0
js_file_result, js_file_error = query_file_list_api(js_file_start, js_file_end)
if js_file_result:
    # js_file_list = [
    #     {
    #         'id': '',
    #         'name': '',
    #         'content': '',
    #     },
    # ]
    js_file_list = js_file_result['list']
    controller_api_dict = get_controller_api_dict(js_file_list)

# 检查项目接口 更新数据库接口 获取数据库中接口
# database_api_list = []
# database_api_result, database_api_error = auto_create_apiurl_api()
# if database_api_error is None:
#     # database_api_list = [
#     #     {
#     #         'id': '',
#     #         'name': '',
#     #         'url': '',
#     #         'is_auth': '',
#     #     },
#     # ]
#     database_api_list = database_api_result['list']

database_api_list = []
# 获取数据库中接口 1.
database_api_result, database_api_error = query_api_url_list_api()
if database_api_result:
    # database_api_list = [
    #     {
    #         'id': '',
    #         'name': '',
    #         'url': '',
    #     },
    # ]
    database_api_list = database_api_result['list']


database_menu_list = []
# 获取菜单 1.0
database_menu_result, database_menu_error = query_menu_list_api()
if database_menu_result:
    # database_menu_list = [
    #     {
    #         "id": '',
    #         "name": '',
    #         "state": '',
    #         "url_id_list": [
    #             {
    #                 'id': '',
    #                 'name': '',
    #                 'url': '',
    #             },
    #         ],
    #     },
    # ]
    database_menu_list = database_menu_result['list']


control_api_result = []
# 处理 控制器 api信息 1.0
if app_package_json and controller_api_dict and database_api_list:
    control_api_result = deal_controller_api_package(app_package_json, controller_api_dict, database_api_list)

# 增加模态框
# control_api_modal_result = []
# if control_api_result and app_package_json:
#     control_api_modal_result = deal_control_api_modal_box(control_api_result, app_package_json)

# 处理 不包含模态框 1.0
if database_menu_list and control_api_result:
    deal_contrast_result_dict(database_menu_list, control_api_result)

# 处理 包含模态框
# if database_menu_list and control_api_modal_result:
#     pass

log_append('app_package_json', len(app_package_json), app_package_error, '')
log_append('controller_api_dict', len(controller_api_dict), js_file_error, '')
log_append('database_api_list', len(database_api_list), database_api_error, '')
log_append('database_menu_list', len(database_menu_list), database_menu_error, '')
log_append('control_api_result', len(control_api_result), '', '')