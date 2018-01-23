#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import requests
import re  
import os

#该类主要用于数据统计以及启动恢复等
class staticLoadNum():
    def __init__(self, url, level_num):
        self.url = url
        self.level_num = level_num
        self.list = list();
        self.file_num = 0;
        self.sum_num = 0;

    def __set_file_num(self, file_num):
        self.file_num = file_num
        

    def data_add(self, sub_data):
        #此处可以增加类型判断
        self.list.append(sub_data)
        self.sum_num += sub_data.sum_num

    def __str__(self):
        static_info = 'The URL is:' + self.url + '\n' +\
                      'Level_num:' + str(self.level_num) +\
                      'Num of Sons:' + str(len(self.list)) +\
                      'File Num:' + str(self.file_num) +\
                      'Sum File Num:' + str(self.sum_num)
        return static_info

class downloadfile():
    ulr_set = set();
    def __init__(self, url, form_str = '.pdf', level_num = 0, max_level = 0):
        self.url = url
        self.max_level = max_level
        self.level_num =  level_num
        self.form_str = form_str
        self.form_file_list = list()
        self.sub_url_list = list()
        self.file_num = 0;
        downloadfile.ulr_set.add(url);

    #网络链接基础方法
    def connect_to_url(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.RequestException as e:
            print('Conneted failed')
            return
        except:
            print('Socket failed!')
            return
        else:
            print(response)
            return response

        

    #解决文件查找方法
    def get_a_href(self, response):
        if (response):
            soup = BeautifulSoup(response.content, "html.parser",from_encoding="iso-8859-1")
            a_list = soup.find_all('a');
            for a_href in a_list:
                #print(a_href)
                hreg = r'(href)'
                pat = re.compile(hreg)
                if (pat.search(str(a_href))):         
                    href_url = a_href['href']
                    if href_url in downloadfile.ulr_set:
                        continue

                    str_form = r'.+' + str(self.form_str) + '$'
                    #print(str_form)
                    pad = re.compile(str_form)
                    if(pad.match(href_url)):
                        #print(href_url)
                        if href_url not in self.form_file_list:
                            self.form_file_list.append(href_url)
                    elif (re.match(r'http', href_url)):
                        if href_url not in self.sub_url_list:
                            self.sub_url_list.append(href_url)        

    #文件下载
    def get_dir_name(self):
        html_form = r'.+\.html$'
        pad = re.compile(html_form)
        if(pad.match(self.url.split('/')[-1])):
            dir_list = self.url.split('/')[3:-1]
        else:
            dir_list = self.url.split('/')[3:]

        dir_name = str(self.level_num)
        for dir_str in dir_list:
            if (len(dir_name) + len(dir_str) > 64):
                break;
            
            dir_str = re.sub('[\/:*?"<>|]','-',dir_str)
            dir_name = dir_name + '_' + dir_str
        return dir_name
    
    def getFile(self, url):
        file_name = url.split('/')[-1]
        print(file_name)
        try:  
            u = urllib.request.urlopen(url)  
        except urllib.error.HTTPError:  
            print(url, "url file not found")  
            return
        except:
            print('File Socket failed!')
            return

        #如果文件存在，则不进行再次写入
        if os.path.exists(file_name):
            print(file_name + 'existed, we passed')
            return

        block_sz = 8192        
        with open(file_name, 'wb') as f:  
            while True:
                buffer = u.read(block_sz)  
                if buffer:  
                    f.write(buffer)
                else:  
                    break
        print ("Sucessful to download" + " " + file_name)
        
    def loadFile(self):
        self.form_file_list.sort()
        form_num = len(self.form_file_list)
        print('The total Form num is', form_num)
        if (form_num != 0):
            dir_name = self.get_dir_name()
            if not os.path.exists(dir_name) :  
                os.mkdir(dir_name)
            os.chdir(os.path.join(os.getcwd(), dir_name))  
            i = 0
            for url in self.form_file_list:
                if (re.match(r'http', url)):
                    url = url
                elif(self.url[-5:] == '.html'):
                    url = self.url[:-len(self.url.split('/')[:-1])] + url 
                else:  
                    url = self.url + url

                print(url)
                self.getFile(url)
                i = i + 1
                rate = format(i/form_num, '.0%')
                print('have load num is:', i, 'and rate:', rate)

    #解决性能问题---进程调度
    def process_load_file(self):
        response = self.connect_to_url()
        self.get_a_href(response)
        self.loadFile()
        if self.level_num > self.max_level:
            return
        for sub_url in self.sub_url_list:
            sub_load_class = downloadfile(sub_url, self.form_str, self.level_num+1, self.max_level)
            sub_load_class.process_load_file()
            print(sub_load_class);

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                               'url:'+ self.url + '\n' +\
                               'level_num:' + str(self.level_num) + '\n' +\
                               'have load file:' + str(len(self.form_file_list)) + '\n'
        return info_str

if __name__=='__main__':
    d_ulr = input('Please input the pdf webSite:')
    level_max = int(input('Please input the max level:'))
    form_str = input('Please input the file form:')
    it_downloadfile = downloadfile(d_ulr, form_str, 0, level_max)
    it_downloadfile.process_load_file()
    print(it_downloadfile)

    
