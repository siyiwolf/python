from bs4 import BeautifulSoup
import re  

def get_a_list(level, soup):
    a_list = list();
    if  soup == None:
        return a_list

    #case0
    return get_a_list_by_interface(filterInterface(level, soup))

    #case1
    #return get_a_list_by_interface(filterDIV(level, soup))
    

def get_a_list_by_interface(filter_interface):
    return filter_interface.get_a_list_by_filter()

class filterInterface():
    def __init__(self, level, soup):
        self.level = level
        self.soup = soup

    def get_a_list_by_filter(self):
        return self.soup.find_all('a')


class filterDIV(filterInterface):
    def filter_div_condition(self, div_str):
        if  div_str == None:
            return False
        
        if  self.level == 0:
            try:
                div_class = div_str['class']
            except:
                #print('div-label have not value of ATTR class')
                return False
        
            if  re.match(r'.*pub_element', str(div_class)):
                return True
            else:
                #print('Match class Failed!')
                return False
                
        return True

    def filter_a_condition(self, a_href_str):
        if  a_href_str == None:
            return False
        
        if  self.level == 1:
            load_str = r'Download Publication'
            pad_load = re.compile(load_str)
            if (pad_load.match(a_href_str)):
                #print ('Match load page Success!')
                return True
            else:
                return False
        
        return True
        
    def get_a_list_by_filter(self):
        a_list = list()
        div_list = self.soup.find_all('div')
        for div_href in div_list:
            if  self.filter_div_condition(div_href):
                a_temp_list = div_href.find_all('a');
                for a_href in a_temp_list:
                    if  self.filter_a_condition(a_href.string):
                        if a_href not in a_list:
                           a_list.append(a_href)
        return a_list
