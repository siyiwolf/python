#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import requests
import json

import staticInfomation
import serializationTool
import loadControlData

class loadFrame():
    max_level = 0
    file_type = ''
    def __init__(self, url, current_dir, level = 0):
        self.current_dir = current_dir
        self.local_data = loadControlData.loadControlData(url, current_dir, level)
        self.static_data = staticInfomation.staticInfomation(current_dir)

    #链接到服务器
    def conect_to_server(self):
        url = self.local_data.get_load_url()
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except:
            print('Connect failed!')
            return
        return response

    #解析响应
    def parse_sub_html(self, response):
        if  response == None:
            return

        #获取文件数
        soup = BeautifulSoup(response.content, "html.parser",from_encoding="GBK")
        file_num = self.local_data.parse_file_url(soup)
        self.static_data.set_file_num(file_num)


    #创建一个子类
    def creat_sub_instance(sub_url, sub_dir, sub_level):
        sub_load_frame = serializationTool.deserialize_data(sub_dir)
        #如果为空，则表示反序列化失败，需要重新创建
        if (sub_load_frame == None):
            sub_load_frame = loadFrame(sub_url, sub_dir, sub_level)
        return sub_load_frame
        
            
    #下载文件
    def assgin_process_task(self):
        #下载文件
        #failed_num = self.local_data.load_all_file()
        #self.static_data.set_failed_num(failed_num)

        #判断是否需要进一步递归，如果完成不进一步查找子链接
        if  self.local_data.is_task_finished():
            return

        #进一步递归
        sub_level = self.local_data.get_level_num() + 1
        sub_dir = self.local_data.get_sub_dir()
        for i in range(self.local_data.get_sub_url_num()):
            sub_url = self.local_data.get_sub_url_base_index(i)
            sub_load_frame = creat_sub_instance(sub_url, sub_dir, sub_level)
            sub_load_frame.process_work_flow()
            print(sub_load_frame)

    #总体流程
    def process_work_flow(self):
        #链接服务器
        response = self.conect_to_server()
        #解析数据
        self.parse_sub_html(response)
        #分配任务
        self.assgin_process_task()
        #序列化
        serializationTool.serialize_data(self.current_dir, self)

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    'Load_data:'+ str(self.local_data) + '\n' +\
                    'local data:' + str(self.static_data)
        return info_str
    
if __name__=='__main__':
   d_ulr = input('Please input the webSite:')
   level_max = int(input('Please input the max level:'))
   file_type = input('Please input the file type:')
   current_dir = os.getcwd() + '\\0_' + file_type[1:] + '_fileA'
   it_downloadfile = loadFrame(d_ulr, current_dir)
   loadFrame.max_level = level_max
   loadFrame.file_type = file_type
   it_downloadfile.process_work_flow()
   print(it_downloadfile)
   input('Please enter to End!')

