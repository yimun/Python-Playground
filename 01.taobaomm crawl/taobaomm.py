#!/usr/bin/env python  
# coding=utf-8


import urllib2
import urllib
import re  
import thread  
import time  
import sys
import os
from stl import Queue

class Spider_Model:

    CODE_TYPE = 'gbk'
    QUEUE_MAX = 100

    def __init__(self):
        self.mmlist = Queue()
        self.enable = False
        self.mylock = thread.allocate_lock()
        
    def __InitHeaders(self):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        return headers
        
    def __GetContent(self,url):
        while True:
            try:
                req = urllib2.Request(url, headers = self.__InitHeaders()) 
                myResponse = urllib2.urlopen(req)
                myPage = myResponse.read()
                break
            except:
                print '####Can not connect!'
                time.sleep(5)
            
        print 'get page ' + url
        # 编码时忽略非法字符
        return myPage.decode(Spider_Model.CODE_TYPE,'ignore') 
    
    u'''获取某一页的所有对象''' 
    def GetListPage(self,page):
        mmurl = 'http://mm.taobao.com/json/request_top_list.htm?type=0&page='
        url = mmurl + str(page)
        codePage = self.__GetContent(url)
        # print codePage
        str_reg = r'<a class="lady-name" href=".*?user_id=(.*?)".*?>(.*?)<'
        myItems = re.findall(str_reg,codePage,re.S)  
        for item in myItems:  
            self.mmlist.enqueue({'id':item[0],'name':item[1]})  
        # print self.mmlist
 
    u'''获取单个对象的图片，存到相应文件夹'''
    def GetImg(self,mm):
        url = r'http://mm.taobao.com/%s.htm' % mm['id']
        content = self.__GetContent(url)
        # print content
        str_reg = r'<img.*?src="(.*?)"'
        myItems = re.findall(str_reg,content,re.S)
        dir_name = 'pic/%s_%s'%(mm['id'],mm['name'])
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        i = 0
        for item in myItems:
            i += 1
            # print 'get ',item
            try:
                urllib.urlretrieve(item, '%s/%d.jpg'%(dir_name,i))
            except:
                print '------------------urlretrieve error '+item+'----------------'
            
    def GetPages(self):
        print '---------Getpages start'
        for i in range(11,4000):
            try:
                self.GetListPage(i)
            except:
                print "####Something wrong in GetListPage()"
                
            while self.mmlist.length() > Spider_Model.QUEUE_MAX:
                print 'GetPages into sleep'
                time.sleep(10);
            
        print '------------All pages is over--------------'
        self.enable = False
            
    def GetImgs(self):
        print '---------GetImgs start'
        while self.enable or not self.mmlist.isEmpty():
            if self.mmlist.isEmpty():
                time.sleep(5)
            else:
                #try:
                self.mylock.acquire() 
                mm = self.mmlist.dequeue()
                self.mylock.release()
                self.GetImg(mm)
                #except:
                  #  print "####Something wrong in GetImage()"
        
    def Start(self):
        print '---------------Begin--------------------'
        self.enable = True
        thread.start_new_thread(self.GetPages,())
        for i in range(1,30):
            thread.start_new_thread(self.GetImgs,())
            # time.sleep(1)
            
        
            
if __name__ == '__main__':
    if not os.path.exists('pic'):
        os.mkdir('pic')
    myModel = Spider_Model()
    myModel.Start()
    while myModel.enable or not myModel.mmlist.isEmpty():
        # print 'There is %d items in Queue'% myModel.mmlist.length()
        time.sleep(1000)
    # myModel.enable = True
    # myModel.GetListPage(34)  
    # myModel.GetImg({u'id':u'687471686',u'name':u'田源源' })
    