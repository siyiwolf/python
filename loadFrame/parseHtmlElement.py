#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re  

def parse_a_label(a_href, root_url):
    try:
        href_value = a_href['href']
    except:
        return

    fig_str = r'#$'
    fig_pattern = re.compile(fig_str)
    if(fig_pattern.match(href_value)):
        try:
            str1 = a_href['onclick']
        except:
             print('a label have not a vaule of ATTR onclick')
             return
          
        m = re.findall("'([^']+)'", str1)
        href_value = m[0]

    if (re.match(r'http', href_value)):
        return href_value

    if (re.match(r'/', href_value)):
        list_href = root_url.split('/')[0:3];
        #print(list_href)
        href_ulr = ''
        for a_href in list_href:
            if (a_href == ''):
                href_ulr = href_ulr + '//'
            else:
                href_ulr =  href_ulr + a_href

        href_ulr = href_ulr + href_value
        return href_ulr
        
    if (re.match(r'\.', href_value)):
        href_ulr = root_url + href_value[1:]
    else:
        href_ulr = root_url + href_value

    return href_ulr
            
            
            
            
        
        
