#!/usr/bin/env python
# coding=utf8

# version:2.0
# windows python 3.3
# author:TClion
# update:2018-01-12
# download tencent manhua,use phantomjs

import os
import time
import requests
from lxml import etree
from selenium import webdriver



header = {
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

class ManHuaDownload():
    def __init__(self):
        self.MainUrl = "http://ac.qq.com/Comic/comicInfo/id/505430" #海贼王主页
        self.OriginUrl = "http://ac.qq.com"
        self.address = "F:\\海贼王\\"          #本地存放漫画的文件夹，请提前建好
        self.S = requests.session()


    #各话的链接
    def GetList(self):
        content = self.S.get(self.MainUrl).content
        page = etree.HTML(content)
        UrlList = page.xpath("//span[@class='works-chapter-item']/a/@href")
        title = page.xpath("//span[@class='works-chapter-item']/a/@title")
        urllist = [self.OriginUrl+x for x in UrlList]
        self.List = list(zip(title,urllist))

    #下载图片
    def DownLoadjpg(self, url, number):
        img = requests.get(url, headers=header)
        with open ('%d.jpg' % number, 'wb') as f:
            for chunk in img.iter_content(1024):
                if chunk:
                    f.write(chunk)

    #储存图片
    def SaveImg(self, title, ImgList):
        newpath = self.address + title.replace('/', '')
        os.mkdir(newpath)
        os.chdir(newpath)
        i = 0
        for u in ImgList:
            self.DownLoadjpg(u,i)
            i += 1
            time.sleep(1)

    #利用PhantomJs和翻页获取图片url
    def GetImgUrl(self):
        for u in self.List:
            title = u[0]
            indexurl = u[1]
            broswer = webdriver.PhantomJS()
            broswer.get(indexurl)
            for i in range(2000, 26000, 2000):            #关键，模拟下拉页面
                broswer.execute_script("window.scrollTo(0, %d);" % i)
                time.sleep(2)
            src = broswer.find_elements_by_class_name('loaded')
            ImgList = []
            for i in src:
                ImgList.append(i.get_attribute('src'))
            broswer.quit()
            self.SaveImg(title, ImgList)
            print(title + ' ' + '下载完成')

if __name__ == '__main__':
    TX = ManHuaDownload()
    TX.GetList()
    TX.GetImgUrl()


