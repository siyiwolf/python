#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import requests
import re  
import os

#该类主要用于数据统计以及启动恢复�?
class staticLoadNum():
    def __init__(self, url, level_num):
        self.url = url
        self.level_num = level_num
        self.list = list();
        self.file_num = 0;
        self.sum_num = 0;
        self.file_failed_num = 0;
        self.sum_failed_num = 0;

    def set_file_num(self, file_num):
        self.file_num = file_num
        self.sum_num += file_num

    def data_add(self, sub_data):
        #此处可以增加类型判断
        self.list.append(sub_data)
        self.sum_num += sub_data.sum_num

    def __str__(self):
        static_info = 'The URL is:' + self.url + '\n' +\
                      'Level_num:' + str(self.level_num) + '\n' +\
                      'Num of Sons:' + str(len(self.list)) + '\n' +\
                      'File Num:' + str(self.file_num) + '\n' +\
                      'Sum File Num:' + str(self.sum_num)
        return static_info

#下载�?
class downloadfile():
    ulr_set = set();
    def __init__(self, url, max_level, form_str, father_dir, level_num = 0):
        self.url = url
        self.max_level = max_level
        self.level_num =  level_num
        self.form_str = form_str
        self.form_file_list = list()
        self.sub_url_list = list()
        self.file_num = 0;
        self.localData = staticLoadNum(url, level_num)    #打包数据
        downloadfile.ulr_set.add(url);

        #规划下载文件存储目录层级
        os.chdir(father_dir)
        load_dir = str(level_num) + '_load_' + form_str[1:]
        
        if not os.path.exists(load_dir):
            os.mkdir(load_dir)
        os.chdir(os.path.join(os.getcwd(), load_dir))
        self.dir_name = os.getcwd()

    def get_local_data(self):
        return self.localData

    #网络链接基础方法
    def connect_to_url(self):
        try:
            response = requests.get(self.url, timeout = 30)
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
            soup = BeautifulSoup(response.content, "html.parser",from_encoding="GBK")
            a_list = self.parser_div_element(soup)
            #a_list = soup.find_all('a')
            for a_href in a_list:
                #a_href 过滤条件
                if (self.filter_a_condition(a_href.string) == False):
                    #print('No Match Condition!,We Pass')
                    continue

                try:
                    href_url = a_href['href']
                except:
                    print('a-label have not a vaule of ATTR href')
                    continue

                if href_url in downloadfile.ulr_set:
                    continue

                #匹配href是否�?
                fig_str = r'#$'
                pad_fig = re.compile(fig_str)
                if(pad_fig.match(href_url)):
                    print('Match # Success!')
                    try:
                        str1 = a_href['onclick']
                    except:
                        print('a label have not a vaule of ATTR onclick')
                        continue
              
                    m = re.findall("'([^']+)'", str1)
                    href_url = m[0]
                    #print(a_href)
                    #print(href_url)
                    
                #文件格式匹配
                str_form = r'.+' + str(self.form_str) + '$'   
                pad = re.compile(str_form)

                #返回上一目录匹配
                sub_dir = r'.*/'                             
                pad_dir = re.compile(sub_dir)
                    
                if(pad.match(href_url)):                                                      #匹配文件，确定找到下载的文件                      
                    #print(debug_href_url)
                    if href_url not in self.form_file_list:
                        self.form_file_list.append(href_url)
                elif (re.match(r'http', href_url)):                                           #匹配子链�?
                    #print('debug http')
                    if href_url not in self.sub_url_list:
                        self.sub_url_list.append(href_url)   
                elif (pad_dir.match(href_url)):                                               #确定是否属于返回上一目录
                    print('debug sub_dir')
                    if(re.match(href_url.split('/')[-2],self.url.split('/')[-3])):            #判断返回到原始的位置
                        print('continue')
                        print(href_url.split('/'))
                        print(self.url.split('/'))
                        continue
                    rHtml_str = self.remove_html()
                    temp_url = rHtml_str + href_url

                    #特殊化处理先
##                  temp_url = 'http://www.bzmfxz.com' + href_url
##                  print(temp_url)
##                  if temp_url not in self.sub_url_list:
##                      self.sub_url_list.append(temp_url)
                    
    #删除html后缀
    def remove_html(self):
        html_form = r'.+\.htm'
        pad = re.compile(html_form)
        end_index = 0
        if(pad.match(self.url.split('/')[-1])):
            end_index = end_index = len(self.url.split('/')[-1])
        return self.url[:end_index]

    def parser_div_element(self, soup):
        a_list = list();
        if (soup == None):
            return a_list

        div_list = soup.find_all('div')
        for div_href in div_list:
            #print(div_href)
            if (self.filter_div_condition(div_href)):
                a_temp_list = div_href.find_all('a');
                #print(a_temp_list)
                for a_href in a_temp_list:
                    if (a_href not in a_list):
                        a_list.append(a_href)
        return a_list

    def filter_div_condition(self, div_str):
        if (div_str == None):
            return False

        if (self.level_num == 0):
            try:
                div_class = div_str['class']
            except:
                print('div-label have not value of ATTR class')
                return False

            if (re.match(r'.*pub_element', str(div_class))):
                return True
            else:
                print('Match class Failed!')
                return False

        return True
            

##    #Case One
##    def filter_a_condition(self, a_href_str):
##        if (a_href_str == None):
##            return False
##
##        if (self.level_num == 0):
##            gjb_str = r'.*\r\nGJB'
##            pad = re.compile(gjb_str)
##            if (pad.match(a_href_str)):
##                print('Match GJB Success!')
##                return True
##            else:
##                return False
##        elif (self.level_num == 1):
##            load_str = r'.*进入下载页面'
##            pad_load = re.compile(load_str)
##            if (pad_load.match(a_href_str)):
##                print ('Match load page Success!')
##                return True
##            else:
##                return False
##        elif (self.level_num == 2):
##            load_str = '.*点击下载'
##            if (re.match(load_str, a_href_str)):
##                print ('Match LOAD Success!')
##                return True
##            else:
##                return False

    #Case Two
    def filter_a_condition(self, a_href_str):
        if (a_href_str == None):
            return False

        if (self.level_num == 1):
            load_str = r'Download Publication'
            pad_load = re.compile(load_str)
            if (pad_load.match(a_href_str)):
                #print ('Match load page Success!')
                return True
            else:
                return False

        return True
    

    #文件下载
    def get_dir_name(self):
##        html_form = r'.+\.html$'
##        pad = re.compile(html_form)
##        if(pad.match(self.url.split('/')[-1])):
##            dir_list = self.url.split('/')[3:-1]
##        else:
##            dir_list = self.url.split('/')[3:]
        dirl = self.remove_html()
        dir_list = self.url.split('/')[3:]
        dir_name = str(self.level_num)
        for dir_str in dir_list:
            if (len(dir_name) + len(dir_str) > 64):
                return dir_name;
            
            dir_str = re.sub('[\/:*?"<>|]','-',dir_str)
            dir_name = dir_name + '_' + dir_str

        return dir_name
    
    def getFile(self, url):
        file_name = url.split('/')[-1]
        #print(file_name)
        try:  
            u = urllib.request.urlopen(url, timeout = 180)  
        except urllib.error.HTTPError:  
            print(url, "url file not found")  
            return
        except:
            print('File Socket failed!')
            return

        #如果文件存在，则不进行再次写�?
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
        print ("Sucessful to download" + " " + file_name)
        
    def loadFile(self):
        #self.form_file_list.sort()
        form_num = len(self.form_file_list)
        self.localData.set_file_num(form_num)
        print('The total Form num is', form_num)
        if (form_num != 0):
            dir_name = self.get_dir_name()
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            cur_dir = os.getcwd()
            os.chdir(os.path.join(cur_dir, dir_name))  
            i = 0
            for url in self.form_file_list:
                if (re.match(r'http', url)):
                    url = url
                elif(self.url[-5:-1] == '.htm'):
                    url = self.url[:-len(self.url.split('/')[:-1])] + url 
                else:  
                    url = self.url + url

                print(url)
                self.getFile(url)
                i = i + 1
                rate = format(i/form_num, '.0%')
                print('have load num is:', i, 'and rate:', rate)
            
            os.chdir(cur_dir)

    #解决性能问题---进程调度
    def process_load_file(self):
        response = self.connect_to_url()
        self.get_a_href(response)
        self.loadFile()
        if self.level_num > self.max_level:
            return
        for sub_url in self.sub_url_list:
            sub_load_class = downloadfile(sub_url, self.max_level, self.form_str, self.dir_name, self.level_num+1)
            sub_load_class.process_load_file()
            self.localData.data_add(sub_load_class.get_local_data())
            print(sub_load_class);

    def __str__(self):
        info_str = 'LoadFile Infomation:\n' +\
                               'url:'+ self.url + '\n' +\
                               'level_num:' + str(self.level_num) + '\n' +\
                               'have load file:' + str(len(self.form_file_list)) + '\n' +\
                               'local data:' + str(self.localData)
        return info_str

if __name__=='__main__':
    d_ulr = input('Please input the pdf webSite:')
    level_max = int(input('Please input the max level:'))
    form_str = input('Please input the file form:')
    it_downloadfile = downloadfile(d_ulr, level_max, form_str, os.getcwd())
    print(os.getcwd())
    it_downloadfile.process_load_file()
    print(it_downloadfile)
    
    
