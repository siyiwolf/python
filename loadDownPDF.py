# coding = UTF-8  
# 爬取大学nlp课程的教学pdf文档课件  http://ccl.pku.edu.cn/alcourse/nlp/  
  
import urllib.request  
import re  
import os
  
# open the url and read  
def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html = page.read()  
    page.close()  
    return html  
  
# compile the regular expressions and find  
# all stuff we need  
def getUrl(html):  
    #reg = r'(Chapter\_\d\d)' #匹配了Chapter_01
    reg = r'(?:href|HREF)="?((?:http://)?.+?\.pdf)'
    #reg = r'([A-Z]\d+)' #匹配了G176200001
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


root_url = 'http://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/IEEE_IROS_2013/media/files/'  
raw_url = 'http://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/IEEE_IROS_2013/media/files/'

#root_url = 'https://www.cc.gatech.edu/~jarek/graphics/papers/'  
#raw_url = 'https://www.cc.gatech.edu/~jarek/graphics/papers/'
#root_url = 'http://www.xyztlab.com/pubs?category=bell143/'  
#raw_url = 'http://www.xyztlab.com/pubs?category=bell143/'
#root_url = 'https://engineering.purdue.edu/ZhangLab/publications/papers/'   
#raw_url = 'https://engineering.purdue.edu/ZhangLab/publications/papers/'
#root_url = 'http://stanford.edu/class/ee367/Winter2016/'
#raw_url = 'http://stanford.edu/class/ee367/Winter2016/' 
#root_url = 'http://people.csail.mit.edu/bkph/AIM/'
#raw_url = 'http://people.csail.mit.edu/bkph/AIM/'
#root_url = 'http://ccl.pku.edu.cn/alcourse/nlp/'
#raw_url = 'http://ccl.pku.edu.cn/alcourse/nlp/' 
  
html = getHtml(raw_url)  
url_lst = getUrl(html)
url_lst.sort()
url_lst.reverse()
print("url_lst", url_lst)
pdf_num = len(url_lst)
  
if not os.path.exists('Intelligent Robots and Systems') :  
    # 文件夹不存在时，再进行创建  
    os.mkdir('Intelligent Robots and Systems')  
os.chdir(os.path.join(os.getcwd(), 'Intelligent Robots and Systems'))  

i = 0
for url in url_lst[:]:  
    url = root_url + url  #形成完整的下载地址  
    getFile(url)
    i = i + 1
    rate = format(i/pdf_num, '.0%')
    print(rate)

