#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import re  
import os

import parseHtmlElement
import filterCondition
import staticInfomation

class downLoadFrame():
    ulr_set = set();
    def __init__(self, url, max_level, current_dir, file_type = '.pdf', level = 0):
        self.url = url
        self.max_level = max_level
        self.file_type = file_type
        self.level = level
        self.file_list = list()
        self.subUlr_list = list()
        self.static_data = staticInfomation.staticInfomation(current_dir);
        downLoadFrame.ulr_set.add(url)

    def get_static_data(self):
        return self.static_data
    
    def conect_to_server(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
        except:
            print('Connect failed!')
            return
        return response

    def is_file_ulr(self, href_value):
        type_str = r'.+' + self.file_type + '$'
        type_pattern = re.compile(type_str)
        if type_pattern.match(href_value):
            return True

        return False

    def remove_html(self):
        html_form = r'.+\.htm'
        pad = re.compile(html_form)
        end_index = 0
        if  pad.match(self.url.split('/')[-1]):
            end_index = end_index = len(self.url.split('/')[-1])
        return self.url[:end_index]
        
    def parse_sub_html(self, response):
        if  response == None:
            return
   
        soup = BeautifulSoup(response.content, "html.parser",from_encoding="GBK")
        a_list = filterCondition.get_a_list(self.level, soup)
        
        root_ulr = self.remove_html()
        for a_href in a_list:
            href_value = parseHtmlElement.parse_a_label(a_href, root_ulr)
            if  href_value == None:
                continue

            if  href_value in downLoadFrame.ulr_set:
                continue
 
            if  self.is_file_ulr(href_value):
                if  href_value not in self.file_list:
                    self.file_list.append(href_value)
            else:
                if  href_value not in self.subUlr_list:
                    self.subUlr_list.append(href_value)

        self.static_data.set_file_num(len(self.file_list));

    def get_file(self, file_ulr):
        #print(file_ulr)
        file_name = format(file_ulr.split('/')[-1])
        file_name = re.sub('[\/:*?"<>|]','-',file_name)     #文件名不支持的字符
        file_ulr = file_ulr.replace(' ', '%20')
        print(file_ulr)
        try:  
            u = urllib.request.urlopen(file_ulr)
        except urllib.error.HTTPError:  
            print("URL file not found")
            self.static_data.updata_failed_num()
            return
        except:
            print('Get URL file failed!')
            self.static_data.updata_failed_num()
            return

        if os.path.exists(file_name):
            print(file_name + ' existed, we passed')
            return

        block_sz = 8192        
        with open(file_name, 'wb') as f:  
            while True:
                buffer = u.read(block_sz)  
                if buffer:  
                    f.write(buffer)
                else:  
                    break
        print ("Sucessful to download " + file_name)
        
    def load_file(self):
        if  len(self.file_list) == 0:
            return
      
        file_dir = self.static_data.get_file_dir(self.file_type)
        if  not os.path.exists(file_dir):
            os.makedirs(file_dir)

        os.chdir(file_dir)                  
        for file_ulr in self.file_list:
            self.get_file(file_ulr);

    def assgin_process_task(self):
        self.load_file()

        if  self.level > self.max_level:
            return

        sub_level = self.level + 1
        index = 0;
        for sub_ulr in self.subUlr_list:
            index += 1
            sub_dir = self.static_data.get_sub_dir(sub_level, index)
            sub_load_file = downLoadFrame(sub_ulr, self.max_level, sub_dir, self.file_type, sub_level)
            sub_load_file.process_work_flow()
            print(sub_load_file)
            self.static_data.add_son_static_data(sub_load_file.get_static_data())

    def process_work_flow(self):
        response = self.conect_to_server()
        self.parse_sub_html(response)
        self.assgin_process_task()

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    'url:'+ self.url + '\n' +\
                    'local data:' + str(self.static_data)
        return info_str
    
if __name__=='__main__':
   d_ulr = input('Please input the webSite:')
   level_max = int(input('Please input the max level:'))
   file_type = input('Please input the file type:')
   current_temp = os.getcwd() + '\\0_' + file_type[1:] + '_file_'
   d_temp = d_ulr
   for i in range(1):
       current_dir = current_temp + str(i+16)
       print(current_dir)
       d_ulr = d_temp + str(i+16)
       print(d_ulr)
       it_downloadfile = downLoadFrame(d_ulr, level_max, current_dir, file_type)
       it_downloadfile.process_work_flow()
       print(it_downloadfile)
       
   input('Please enter to End!')
