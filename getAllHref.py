# coding = UTF-8  
import urllib.request  
import re  
import os

import requests
from bs4 import BeautifulSoup
import re
#import socket.gaierror

level_max = 2;
ulr_dict = dict();
ulr_set =set();

def getUrl(html):  
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)  
    url_lst = url_re.findall(html.decode('UTF-8', 'ignore'))  #匹配的数组  
    return(list(set(url_lst)))  #把重复项去掉  
  
def getFile(url):  
    file_name = url.split('/')[-1]  
    try:  
        u = urllib.request.urlopen(url)  
    except urllib.error.HTTPError:  
        print(url, "url file not found")  
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

def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html = page.read()  
    page.close()  
    return html  

def getUrl(html):  
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    url_re = re.compile(reg)  
    url_lst = url_re.findall(html.decode('UTF-8', 'ignore'))  #匹配的数组  
    return(list(set(url_lst)))  #把重复项去掉  
  
def getFile(url):  
    file_name = url.split('/')[-1]  
    try:  
        u = urllib.request.urlopen(url)  
    except urllib.error.HTTPError:  
       #碰到了匹配但不存在的文件时，提示并返回  
        print(url, "url file not found")  
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

def loadFile(html, dir_name, root_url):
    url_lst = getUrl(html)
    url_lst.sort()
    pdf_num = len(url_lst)
    print('The total PDF num is', pdf_num)
    if (pdf_num != 0):
        print("url_lst", url_lst)
        if not os.path.exists(dir_name) :  
            # 文件夹不存在时，再进行创建  
            os.mkdir(dir_name)
        os.chdir(os.path.join(os.getcwd(), dir_name))  
        i = 0
        for url in url_lst[begin_num:pdf_num-1]:
            if (re.match(r'http://', url)):
                url = url
            else:
                url = root_url + url
            getFile(url)
            i = i + 1
            rate = format((i + begin_num)/pdf_num, '.0%')
            print('have load num is:', (i+begin_num), 'and rate:', rate)

def getAllHref(url):
    try:
        response = requests.get(url);
        response.raise_for_status();
        #print('Try finshed')
    except requests.RequestException as e:
        print('Conneted failed')
        #print(e.reason)
    except:
        print('Socket failed!')
    else:
        level_num = ulr_dict.get(url)
        print(level_num)
        loadFile(response.content, str(level_num), url)
        soup = BeautifulSoup(response.content, "html.parser",from_encoding="iso-8859-1")
        a_list = soup.find_all('a');
        for a_href in a_list:
            #print(a_href)
            hreg = r'(href)'
            pat = re.compile(hreg)
            mat = pat.search(str(a_href))
            if (mat):
                a_ulr = a_href['href']
                reg = r'http://'
                pattern = re.compile(reg);
                match =  pattern.match(a_ulr);
                if (match):
                    if (a_ulr not in ulr_dict) and (level_num < level_max):
                        ulr_dict[a_ulr] = level_num + 1;
                        print(a_ulr,':', ulr_dict[a_ulr]);
                        getAllHref(a_ulr)
#d_ulr = "https://homes.cs.washington.edu/~mcakmak/#!/pubs"
level_max = int(input('Please input the max level:'))
d_ulr = input('Please input the pdf webSite:')
begin_num = (int)(input('Please input the begin num:'))
ulr_dict[d_ulr] = 0
print(ulr_dict)
getAllHref(d_ulr)

        
