# coding = UTF-8  
  
import urllib.request  
import re  
import os


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


def loadFile(html, dir_name, root_url):
    url_lst = getUrl(html)
    url_lst.sort()
    print("url_lst", url_lst)
    pdf_num = len(url_lst)
  
    if not os.path.exists(dir_name) :  
        # 文件夹不存在时，再进行创建  
        os.mkdir(dir_name)  
    os.chdir(os.path.join(os.getcwd(), dir_name))  
    i = 0
    for url in url_lst[307:pdf_num-42]:  
        url = root_url + url
        getFile(url)
        i = i + 1
        rate = format(i/pdf_num, '.0%')
        print(rate)


