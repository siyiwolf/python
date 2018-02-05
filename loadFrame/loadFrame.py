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
    def __init__(self, url, level_max, current_dir, type_file = '.pdf', level = 0):
        self.current_dir = current_dir
        self.local_data = loadControlData.loadControlData(url, level_max, current_dir, type_file, level)
        self.static_data = staticInfomation.staticInfomation()
        

    #闁剧偓甯撮崚鐗堟箛閸斺€虫珤
    def conect_to_server(self):
        url = self.local_data.get_load_url()
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except:
            print('Connect failed!')
            return
        return response

    #鐟欙絾鐎介崫宥呯安
    def parse_sub_html(self, response):
        if  response == None:
            return

        #閼惧嘲褰囬弬鍥︽閺?
        soup = BeautifulSoup(response.content, "html.parser",from_encoding="GBK")
        file_num = self.local_data.parse_file_url(soup)
        self.static_data.set_file_num(file_num)
        
    def get_static_data(self):
        return self.static_data

            
    #娑撳娴囬弬鍥︽
    def assgin_process_task(self):
        #娑撳娴囬弬鍥︽
        failed_num = self.local_data.load_all_file()
        self.static_data.set_failed_num(failed_num)

        #閸掋倖鏌囬弰顖氭儊闂団偓鐟曚浇绻樻稉鈧銉┾偓鎺戠秺閿涘苯顩ч弸婊冪暚閹存劒绗夋潻娑楃濮濄儲鐓￠幍鎯х摍闁剧偓甯?
        if  self.local_data.is_task_finished():
            return

        #鏉╂稐绔村銉┾偓鎺戠秺
        sub_level = self.local_data.get_level_num() + 1
        sub_url_list = self.local_data.get_sub_url_list()
        index = 0
        for sub_url in sub_url_list:
            index += 1
            sub_dir = self.local_data.get_sub_dir_base_index(index)
            #sub_load_frame = self.creat_sub_instance(sub_url, sub_dir, sub_level)
            sub_load_frame = serializationTool.deserialize_data(sub_dir)
            if  sub_load_frame == None:
                sub_load_frame = loadFrame(sub_url, loadControlData.loadControlData.max_level, sub_dir, loadControlData.loadControlData.file_type, sub_level)
                self.static_data.add_son_static_data(sub_load_frame.get_static_data())
            else:
                print('De-Serialize Success!')
                self.static_data.add_son_static_data(sub_load_frame.get_static_data())
                continue
            
            sub_load_frame.process_work_flow()
            print(sub_load_frame)

    #閹缍嬪ù浣衡柤
    def process_work_flow(self):
        #闁剧偓甯撮張宥呭閸?
        response = self.conect_to_server()
        #鐟欙絾鐎介弫鐗堝祦
        self.parse_sub_html(response)
        #閸掑棝鍘ゆ禒璇插
        self.assgin_process_task()
        #鎼村繐鍨崠?
        serializationTool.serialize_data(self.current_dir, self)

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    '   Load_data:'+ str(self.local_data) + '\n' +\
                    '   local data:' + str(self.static_data)
        return info_str
    
if __name__=='__main__':
   d_ulr = input('Please input the webSite:')
   level_max = int(input('Please input the max level:'))
   file_type = input('Please input the file type:')
   current_dir = os.getcwd() + '\\0_' + file_type[1:] + '_file'
   it_downloadfile = loadFrame(d_ulr, level_max, current_dir, file_type)
   it_downloadfile.process_work_flow()
   print(it_downloadfile)
   input('Please enter to End!')

