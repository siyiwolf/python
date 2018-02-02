#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import re  
import os

import loadFrame
import filterCondition
import parseHtmlElement

class loadControlData():
    url_set = set()
    def __init__(self, url, current_dir, level = 0):
        self.url = url
        self.current_dir = current_dir
        self.level = level
        self.file_list = list()
        self.subUlr_list = list()

    def get_load_url(self):
        return self.url
        
    def get_sub_url_num(self):
        return (len(self.subUlr_list))

    def get_sub_url_base_index(self, index):
        sub_path = self.current_dir + '\\' + str(self.level) + '_' + str(index)
        return sub_path
        
    def is_file_ulr(self, href_value):
        type_str = r'.+' + loadFrame.loadFrame.file_type + '$'
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

    def parse_file_url(self, soup):
        if  soup == None:
            return

        a_list = filterCondition.get_a_list(self.level, soup)
        root_ulr = self.remove_html()
        for a_href in a_list:
            href_value = parseHtmlElement.parse_a_label(a_href, root_ulr)
            if  href_value == None:
                continue

            if  href_value in loadControlData.url_set:
                continue

            if  self.is_file_ulr(href_value):
                if  href_value not in self.file_list:
                    self.file_list.append(href_value)
            else:
                if  href_value not in self.subUlr_list:
                    self.subUlr_list.append(href_value)
      

    def get_file(self, file_ulr):
        file_name = file_ulr.split('/')[-1]
        try:  
            u = urllib.request.urlopen(file_ulr, timeout = 180)  
        except:
            print('Get URL file failed!')
            return False

        if os.path.exists(file_name):
            print(file_name + ' existed, we passed')
            return True

        block_sz = 8192        
        with open(file_name, 'wb') as f:  
            while True:
                buffer = u.read(block_sz)  
                if buffer:  
                    f.write(buffer)
                else:  
                    break
        print ("Sucessful to download " + file_name)
        return True

    def get_file_dir(self):
        file_path =self.current_dir + '\\' + loadFrame.loadFrame.file_type[1:] + '_file'
        return file_path

    def load_all_file(self):
        failed_num = 0
        if  len(self.file_list) == 0:
            return failed_num
      
        file_dir = self.get_file_dir()
        if  not os.path.exists(file_dir):
            os.makedirs(file_dir)

        os.chdir(file_dir)                  
        for file_ulr in self.file_list:
            if (self.get_file(file_ulr) == False):
                failed_num += 1

        return failed_num

    def is_task_finished(self):
        return (self.level == loadFrame.loadFrame.max_level)

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    'url:'+ self.url + '\n' +\
                    'current_dir:'+ self.current_dir + '\n' +\
                    'level:' + str(self.level)
        return info_str

