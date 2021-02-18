#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/21
# file: conn_test.py
# Email:
# Author: 唐政 
import json
import os
import pypyodbc
import requests
from app import BASE_PATH
from utils import get_last_data_flag, set_last_data_flag, get_pid, show_msg
import os
import sys
import winerror
import win32serviceutil
import win32service
import win32event
import servicemanager
import json
import inspect
from PythonService import getLogger
this_file = inspect.getfile(inspect.currentframe())

BASE_PATH = os.path.abspath(os.path.dirname(this_file))

def load_config(logger=None):
    import json

    try:
        config = json.load(open(os.path.join(BASE_PATH, "config.json")))
    except Exception as e:
        logger.error(e)
    return config

def run_script(config, logger=None):
    import importlib
    try:
        programe = importlib.import_module("%s" % config["script"])
    except Exception as e:
        logger.error(e)
    programe.run(config, logger)

def getLogger():
    import logging
    import os

    logger = logging.getLogger('[PythonService]')

    # handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
    from logging import handlers
    handler = handlers.TimedRotatingFileHandler(os.path.join(BASE_PATH, "service.log"), when='h', interval=5,
                                                backupCount=30)

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

def run(config, logger):
    """
    :param config:
    :return:
    """

    path = config["dbpath"]
    conn = pypyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + path + ";Uid=;Pwd=;")
    try:
        cursor = conn.cursor()
        last_time = get_last_data_flag()
        if last_time:
            SQL = "select * from AnalyseResult where Time>#%s#;" % last_time
            print(SQL)
        else:
            SQL = "select * from AnalyseResult;"
        ana_list = []
        for row in cursor.execute(SQL):
            ana_list.append({
                "Time": row[4],
                "Result_C": row[6],
                "Result_S": row[7],
            })

        for ana in ana_list:
            success = upload_data_to_jhy(config, ana, logger)

            if success:

                set_last_data_flag(
                    "%s" % (ana.get("Time").strftime("%Y-%m-%d, %H:%M:%S")))

            else:
                show_msg(u"错误", u"上传化验信息失败，请查看网络。或联系开发人员", config, logger)
                break
    except Exception as e:
        raise e
    finally:
        conn.close()

config = load_config()
# run_script(config)
logger = getLogger()

run(config, logger)
