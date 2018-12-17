# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:16:24 2018

@author: Wang
"""

import re
import requests
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
p=ThreadPoolExecutor(30) #定义线程池最多容纳30个线程

#链接到第一ppt免费ppt模板的界面
def get_Index(url):
    respose=requests.get(url)
    if respose.status_code==200:
        print("网站链接成功")
        return respose.text
    else:
        print("无法链接到模板界面")
        return

#解析获取到的html代码，获取当前页面每个ppt模板的链接
def parse_Index(res):
    res=res.result()
    #获取模板链接
    urls=re.findall(r'h2.*?href="(.*?)"',res,re.S)
    #print(urls)
    for url in urls:
        #提交到线程池
        p.submit(get_Detail(url))

#模板详情界面        
def get_Detail(url):
    if not url.startswith('http'):
        url='http://www.1ppt.com%s' %url
    detailRespose=requests.get(url)
    if detailRespose.status_code==200:
        ppt_url=re.findall(r'class="downurllist".*?href="(.*?)"',detailRespose.text,re.S)
        ppt_url=ppt_url[0]
        if ppt_url:
            print(ppt_url)
            save(ppt_url)
            '''
            ppt=requests.get(ppt_url)
            if ppt.status_code==200:
                m=hashlib.md5();
                m.update(ppt_url.encode('utf-8'))
                m.update(str(time.time()).encode('utf-8'))
                filename=r'%s.zip' % m.hexdigest()
                filepath=r'D:\ppt\%s' %filename
                with open(filepath,'wb') as f:
                    f.write(ppt.content)
            else:
                print("无法下载")
                return
            '''    
    else:
        print("无法连接的详情界面")
        return
        
#将文件保存
def save(ppt_url):
    ppt=requests.get(ppt_url)
    if ppt.status_code==200:
        m=hashlib.md5();
        m.update(ppt_url.encode('utf-8'))
        m.update(str(time.time()).encode('utf-8'))
        filename=r'%s.zip' % m.hexdigest()
        filepath=r'D:\\ppt\\%s' %filename
        with open(filepath,'wb') as f:
            f.write(ppt.content)
    else:
        print("无法下载")
        return
        
def main():
    for i in range(5,7):
        p.submit(get_Index,'http://www.1ppt.com/moban/ppt_moban_%s.html' % i ).add_done_callback(parse_Index)

if __name__=='__main__':
    main()        

