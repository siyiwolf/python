import json
import os

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import re  
import os
from bs4 import BeautifulSoup
import requests
import json


import filterCondition
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
        #先查看文件是否存在，如果文件存在，则直接返回，不用试着进行http请求，提高效率
        file_name = file_ulr.split('/')[-1]
        file_name = re.sub('[\/:*?"<>|]','-',file_name)     #文件名不支持的字符
        if os.path.exists(file_name):
            print(file_name + ' existed, we passed')
            return True

        file_ulr = file_ulr.replace(' ', '%20')             #空格转换为%20，满足链接条件
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
                    'url:'+ self.url + '\n' +\
                    'current_dir:'+ self.current_dir + '\n' +\
                    'level:' + str(self.level)
        return info_str


class loadFrame():
    def __init__(self, url, level_max, current_dir, type_file = '.pdf', level = 0):
        self.current_dir = current_dir
        self.local_data = loadControlData(url, level_max, current_dir, type_file, level)
        self.static_data = staticInfomation()
        

    #閾炬帴鍒版湇鍔″櫒
    def conect_to_server(self):
        url = self.local_data.get_load_url()
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except:
            print('Connect failed!')
            return
        return response

    #瑙ｆ瀽鍝嶅簲
    def parse_sub_html(self, response):
        if  response == None:
            return

        #鑾峰彇鏂囦欢鏁?
        soup = BeautifulSoup(response.content, "html.parser",from_encoding="GBK")
        file_num = self.local_data.parse_file_url(soup)
        self.static_data.set_file_num(file_num)
        
    def get_static_data(self):
        return self.static_data

    #鍒涘缓涓€涓瓙绫?
    def creat_sub_instance(self, sub_url, sub_dir, sub_level):
        sub_load_frame = serializationTool.deserialize_data(sub_dir)
        print(sub_load_frame)
        #濡傛灉涓虹┖锛屽垯琛ㄧず鍙嶅簭鍒楀寲澶辫触锛岄渶瑕侀噸鏂板垱寤?
        if (sub_load_frame == None):
            sub_load_frame = loadFrame(sub_url, loadControlData.loadControlData.max_level, sub_dir, loadControlData.loadControlData.file_type, sub_level)
            self.static_data.add_son_static_data(sub_load_frame.get_static_data())
        return sub_load_frame
        
            
    #涓嬭浇鏂囦欢
    def assgin_process_task(self):
        #涓嬭浇鏂囦欢
        #failed_num = self.local_data.load_all_file()
        #self.static_data.set_failed_num(failed_num)

        #鍒ゆ柇鏄惁闇€瑕佽繘涓€姝ラ€掑綊锛屽鏋滃畬鎴愪笉杩涗竴姝ユ煡鎵惧瓙閾炬帴
        if  self.local_data.is_task_finished():
            return

        #杩涗竴姝ラ€掑綊
        sub_level = self.local_data.get_level_num() + 1
        sub_url_list = self.local_data.get_sub_url_list()
        index = 0
        for sub_url in sub_url_list:
            index += 1
            sub_dir = self.local_data.get_sub_dir_base_index(index)
            sub_load_frame = self.creat_sub_instance(sub_url, sub_dir, sub_level)
            sub_load_frame.process_work_flow()
            print(sub_load_frame)

    #鎬讳綋娴佺▼
    def process_work_flow(self):
        #閾炬帴鏈嶅姟鍣?
        response = self.conect_to_server()
        #瑙ｆ瀽鏁版嵁
        self.parse_sub_html(response)
        #鍒嗛厤浠诲姟
        self.assgin_process_task()
        #搴忓垪鍖?
        serializationTool.serialize_data(self.current_dir, self)

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                    'Load_data:'+ str(self.local_data) + '\n' +\
                    'local data:' + str(self.static_data)
        return info_str
    

class staticInfomation():
    def __init__(self):
        self.son_list = list()
        self.file_num = 0
        self.failed_num = 0


    def set_file_num(self, file_num):
        self.file_num = file_num

    def get_file_num(self, file_num):
        return self.file_num

    def static_sum_num(self):
        sumNum = self.file_num;
        for son_static in self.son_list:
            sumNum += son_static.static_sum_num()
        return sumNum

    def static_failed_sum(self):
        sumFailedNum = self.failed_num;
        for son_static in self.son_list:
            sumFailedNum += son_static.static_failed_sum()

        return sumFailedNum
        
    def set_failed_num(self, failed_num):
        self.failed_num = failed_num;

    def add_son_static_data(self, son_data):
        self.son_list.append(son_data)

    def __str__(self):
        static_info = 'The static information is' +  '\n' +\
                      'Num of Sons:' + str(len(self.son_list)) + '\n' +\
                      'File Num:' + str(self.file_num) + '\n' +\
                      'Sum File Num:' + str(self.static_sum_num()) + '\n' +\
                      'Failed Num:' + str(self.failed_num) + '\n' +\
                      'Failed Sum Num:' + str(self.static_failed_sum())
        return static_info

class Point():
    p_id = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        Point.p_id += 1


class D3Point():
    d_id = 0
    def __init__(self, x, y, z):
        self.point = Point(x, y)
        self.z = z
        D3Point.d_id += 1

classes = {
    'loadFrame' : loadFrame,
    'loadControlData' : loadControlData,
    'staticInfomation' : staticInfomation,
    'Point' : Point,
    'D3Point' : D3Point
    
}

          
def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if  clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls) # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
            return obj
    else:
        return d

#序列化
def serialize_data(dir_name, obj):
    if  not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file_name = dir_name + '\\file.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(obj, f, default=serialize_instance)


#反序列化
def deserialize_data(dir_name):
    file_name = dir_name + '\\file.json'
    #判断是否存在文件
    if  os.path.exists(file_name):
        #进行反序列化
        with open(file_name, encoding='utf-8') as f:
            obj = json.load(f, object_hook=unserialize_object)
            return obj
    else:
        return None



if __name__ == '__main__':
    d = D3Point(9,5,9)
    dir_name = 'E:\\'
    serialize_data(dir_name, d)
    k = deserialize_data(dir_name)
    print(k.z)
    
##    it_downloadfile = loadFrame('E:\\', 0, 'E:\\')
##    serialize_data(dir_name, it_downloadfile)
##    c = deserialize_data(dir_name)
##
##    it_downloadfile = staticInfomation()
##    serialize_data(dir_name, it_downloadfile)
##    c = deserialize_data(dir_name)
##    print(c.failed_num)
##    
    
