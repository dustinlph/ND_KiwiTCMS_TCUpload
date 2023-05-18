# coding=utf-8
"""
@Project: KiwiTCMS_TCUpload
@File: /create_tc.py
@Author: Dustin Lin
@Created on: 2023/5/18 15:52:44
"""
from tcms_api import TCMS
import configparser
import os
import csv
import time
import sys


class TCCreator:
    def __init__(self):
        self.rpc_client = TCMS()

    def kiwi_login(self, dict_value):
        self.rpc_client.exec.Auth.login(dict_value['user'], dict_value['password'])
        print("Login successfully")

    def kiwi_logout(self):
        self.rpc_client.exec.Auth.logout()
        print("Logout successfully")

    def csv_reader(self, dict_value):
        str_file_path = os.path.join(os.getcwd(), 'template', dict_value['file_name'])
        obj_file = open(str_file_path, encoding='utf-8', errors='ignore')
        obj_data = csv.reader(obj_file)
        list_data = []
        for line in obj_data:
            list_data.append(line)
        obj_file.close()
        return list_data

    def data_transfer(self, dict_value):
        list_pre_data = dict_value['rawdata']
        list_final_data = []
        for tc in range(1, len(list_pre_data)):
            dict_temp = {}
            dict_temp['product'] = int(list_pre_data[tc][0])
            dict_temp['category'] = int(list_pre_data[tc][1])
            dict_temp['summary'] = list_pre_data[tc][2]
            dict_temp['text'] = list_pre_data[tc][3]
            dict_temp['case_status'] = int(list_pre_data[tc][4])
            dict_temp['priority'] = int(list_pre_data[tc][5])
            list_final_data.append(dict_temp)
        return list_final_data

    def tc_create(self, dict_value):
        list_result = []
        for tc in range(len(dict_value['tc_list'])):
            list_result.append(self.rpc_client.exec.TestCase.create(dict_value['tc_list'][tc]))
            # print(dict_value['tc_list'][tc])
            time.sleep(0.1)
            int_total_case = tc
        print('{} Testcase created successfully'.format(int_total_case + 1))
        print(list_result)
        return list_result

    def data_transfer2(self, dict_value):
        """
        Case status:  [{'id': 1, 'name': 'PROPOSED', 'description': ''},
                        {'id': 2, 'name': 'CONFIRMED', 'description': ''},
                        {'id': 3, 'name': 'DISABLED', 'description': ''},
                        {'id': 4, 'name': 'NEED_UPDATE', 'description': ''}]

        """
        list_pre_data = dict_value['rawdata']
        list_final_data = []
        for tc in range(1, len(list_pre_data)):
            dict_temp = {}
            int_tc_product_id = self.rpc_client.exec.Product.filter({'name': list_pre_data[tc][0]})[0]['id']
            time.sleep(0.1)
            list_category = self.rpc_client.exec.Category.filter({'product_id': int_tc_product_id})
            time.sleep(0.1)
            int_tc_category_id = None
            for ca in range(len(list_category)):
                if list_pre_data[tc][1] == list_category[ca]['name']:
                    int_tc_category_id = list_category[ca]['id']
                else:
                    pass
                """
                if int_tc_category_id is None:
                    int_tc_category_id = self.rpc_client.exec.Category.filter({'name': '--default--', 'product_id': int_tc_product_id})[0]['id']
                    time.sleep(0.1)
                else:
                    pass
                """
            dict_temp['product'] = int_tc_product_id
            dict_temp['category'] = int_tc_category_id
            dict_temp['summary'] = list_pre_data[tc][2]
            dict_temp['text'] = list_pre_data[tc][3]
            dict_temp['case_status'] = 2
            dict_temp['priority'] = 1
            list_final_data.append(dict_temp)
        return list_final_data

    def tc_delete(self, dict_value):
        int_total_tc = 0
        for tc in range(len(dict_value['tc_list'])):
            self.rpc_client.exec.TestCase.remove({'id': dict_value['tc_list'][tc]['id']})
            int_total_tc = tc
        print('{} Testcase deleted successfully'.format(int_total_tc + 1))

    def result_write(self, dict_value):
        list_filename = dict_value['file_name'].split('.')
        str_result_file = list_filename[0] + '_TC_result.txt'
        str_file_path = os.path.join(os.getcwd(), 'result', str_result_file)
        obj_file = open(str_file_path, 'w')
        obj_file.write(str(dict_value['tc_result']))
        obj_file.close()


if __name__ == '__main__':
    argv = sys.argv[1:]
    csv_filename = argv[0]

    tcms_config_path: str = os.path.join(os.path.expanduser('~'), '.tcms.conf')
    tcms_config = configparser.ConfigParser()
    # print(tcms_config_path)
    tcms_config.read(tcms_config_path, encoding='utf-8')

    username: str = tcms_config['tcms']['username']
    password: str = tcms_config['tcms']['password']

    job = TCCreator()
    job.kiwi_login({'user': username, 'password': password})

    list_csv_data = job.csv_reader({'file_name': csv_filename})
    list_dict_data = job.data_transfer2({'rawdata': list_csv_data})

    list_result = job.tc_create({'tc_list': list_dict_data})
    # job.tc_delete({'tc_list': list_result})
    job.result_write({'file_name': csv_filename, 'tc_result': list_result})

    job.kiwi_logout()
