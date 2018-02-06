#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import re  
import os

import loadFrame
import filterInterface
import parseHtmlElement

class loadControlData():
    url_set = set()
    max_level = 0
    file_type = ''
    def __init__(self, url, level_max, current_dir, type_file = '.pdf', level = 0):
        self.url = url
        self.current_dir = current_dir
        self.level = level
        self.file_list = list()
        self.subUlr_list = list()
        loadControlData.max_level = level_max
        loadControlData.file_type = type_file

    def get_level_num(self):
        return self.level

    def get_load_url(self):
        return self.url
        
    def get_sub_url_num(self):
        return (len(self.subUlr_list))

    def get_sub_url_list(self):
        return self.subUlr_list

    def get_sub_dir_base_index(self, index):
        sub_path = self.current_dir + '\\' + str(self.level) + '_' + str(index)
        return sub_path
        
    def is_file_ulr(self, href_value):
        type_str = r'.+' + loadControlData.file_type + '$'
        type_pattern = re.compile(type_str)
        #print(href_value)
        if type_pattern.match(href_value):
            #print('Match pdf success!')
            return True

        return False

    def remove_html(self):
        html_form = r'.+\.htm'
        pad = re.compile(html_form)
        end_index = 0
        if  pad.match(self.url.split('/')[-1]):
            end_index = len(self.url) - len(self.url.split('/')[-1])

        print(self.url[:end_index])
        return self.url[:end_index]

    def parse_file_url(self, soup):
        if  soup == None:
            return 0

        a_list = filterInterface.get_a_list(self.level, soup)
        root_ulr = self.remove_html()
        #print(root_ulr)
        #print(a_list)
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
        return len(self.file_list)

    def get_file(self, file_ulr):
        #先查看文件是否存在，如果文件存在，则直接返回，不用试着进行http请求，提高效率
        file_name = file_ulr.split('/')[-1]
        file_name = re.sub('[\/:*?"<>|]','-',file_name)     #文件名不支持的字符
        if os.path.exists(file_name):
            print(file_name + ' existed, we passed')
            return True

        file_ulr = file_ulr.replace(' ', '%20')             #空格转换为%20，满足链接条件
        #print(file_ulr)
        try:  
            u = urllib.request.urlopen(file_ulr, timeout = 180)  
        except:
            print('Get URL file failed!')
            return False

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
        file_path =self.current_dir + '\\' + loadControlData.file_type[1:] + '_file'
        return file_path

    def load_all_file(self):
        failed_num = 0
        if  len(self.file_list) == 0:
            return failed_num
        print(self.file_list)
        file_dir = self.get_file_dir()
        if  not os.path.exists(file_dir):
            os.makedirs(file_dir)

        os.chdir(file_dir)                  
        for file_ulr in self.file_list:
            if (self.get_file(file_ulr) == False):
                failed_num += 1

        return failed_num

    def is_task_finished(self):
        return (self.level == loadControlData.max_level)

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    '        url:'+ self.url + '\n' +\
                    '        current_dir:'+ self.current_dir + '\n' +\
                    '        level:' + str(self.level)
        return info_str

