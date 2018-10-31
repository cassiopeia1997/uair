# -*-coding:utf-8-*-  
#-*-encoding=utf-8
import sys
 

# from selenium import webdriver
# from bs4 import BeautifulSoup
# import requests
# import os

# class AlbumCover():

    # def __init__(self):
        # self.init_url = "http://www.nitrafficindex.com/traffic/getRoadIndex.do" #请求网址
        # self.folder_path = "C:/Users/cassiopeia/Desktop/uair/temp1" #想要存放的文件目录

    # def save_img(self, url, file_name):  ##保存图片
        # print('开始请求图片地址，过程会有点长...')
        # img = self.request(url)
        # print('开始保存图片')
        # f = open(file_name, 'ab')
        # f.write(img.content)
        # print(file_name, '图片保存成功！')
        # f.close()

    # def request(self, url):  # 封装的requests 请求
        # r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        # return r

    # def mkdir(self, path):  ##这个函数创建文件夹
        # path = path.strip()
        # isExists = os.path.exists(path)
        # if not isExists:
            # print('创建名字叫做', path, '的文件夹')
            # os.makedirs(path)
            # print('创建成功！')
            # return True
        # else:
            # print(path, '文件夹已经存在了，不再创建')
            # return False

    # def get_files(self, path):  # 获取文件夹中的文件名称列表
        # pic_names = os.listdir(path)
        # return pic_names

    # def spider(self):
        # print("Start!")
        # driver = webdriver.PhantomJS()
        # driver.get(self.init_url)
        # print('oo')
        # driver.switch_to.frame("g_iframe")
        # html = driver.page_source
        # print('ok!')
        # self.mkdir(self.folder_path)  # 创建文件夹
        # print('changing')
        # os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        # file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list

        # all_li = BeautifulSoup(html, 'lxml').find(id='m-song-module').find_all('li')
        # # print(type(all_li))

        # for li in all_li:
            # album_img = li.find('img')['src']
            # album_name = li.find('p', class_='dec')['title']
            # album_date = li.find('span', class_='s-fc3').get_text()
            # end_pos = album_img.index('?')
            # album_img_url = album_img[:end_pos]

            # photo_name = album_date + ' - ' + album_name+'.jpg'
            # print(album_img_url, photo_name)

            # if photo_name in file_names:
                # print('图片已经存在，不再重新下载')
            # else:
                # self.save_img(album_img_url, photo_name)

# album_cover = AlbumCover()
# album_cover.spider()
#coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import io
import time
from selenium import webdriver
import re
class Road():
	def __init__(self,name,startName,endName,avgSpeed,roadGarde):
		self.name=name
		self.startName=startName
		self.endName=endName
		self.avgSpeed=avgSpeed
		self.roadGrade=roadGrade
	def savefile(self):
		print("saving")
class AlbumCover():

	def __init__(self):
		self.init_url = "http://www.nitrafficindex.com" #请求网址
		self.folder_path = "C:\Desktop\Uair\Data" #想要存放的文件目录

	def save_img(self, url, file_name):  ##保存图片
		print('start crawling...')
		img = self.request(url)
		print('start saving')
		f = open(file_name, 'ab')
		f.write(img.content)
		print(file_name, 'ok！')
		f.close()

	def request(self, url):  # 封装的requests 请求
		r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
		return r

	def mkdir(self, path):  ##这个函数创建文件夹
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			print('创建名字叫做', path, '的文件夹')
			os.makedirs(path)
			print('创建成功！')
			return True
		else:
			print(path, '文件夹已经存在了，不再创建')
			return False

	def get_files(self, path):  # 获取文件夹中的文件名称列表
		pic_names = os.listdir(path)
		return pic_names

	def spider(self):
		print("Start!")
		driver = webdriver.Chrome()
		driver.get(self.init_url)
		driver.switch_to.frame("mainIframe")
		driver.find_element_by_xpath("//*[@id='div_traffic']/div[1]/div[3]/ul/li[3]/a").click()
		i=0
		time.sleep(3)
		#html = driver.page_source
		
		normal_window = driver.current_window_handle
		html = driver.page_source
		tr_td = BeautifulSoup(html, 'lxml')
		for i in range(9):
			id_name="datagrid-row-r6-2-"+str(i)
			all_td=tr_td.find(id=id_name).find_all('td')
			Road(all_td[0].get_text(),all_td[1].get_text(),all_td[2].get_text(),all_td[3].get_text(),all_td[4].get_text()).savefile()
			print(all_td[0].get_text(),all_td[1].get_text(),all_td[2].get_text(),all_td[3].get_text(),all_td[4].get_text())
        
"""
        #file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list
        i=0
        all_li = BeautifulSoup(html, 'lxml').find(id='div_traffic').find_all('li')
"""
'''
        for li in all_li:
            album_img = li.find('img')['src']
            album_name = li.find('p', class_='dec')['title']
            album_date = li.find('span', class_='s-fc3').get_text()
            end_pos = album_img.index('?')
            album_img_url = album_img[:end_pos]

            photo_name = album_date + ' - ' + album_name.replace('/', '').replace(':', ',') + '.jpg'
            print(album_img_url, photo_name)

            if photo_name in file_names:
                print('图片已经存在，不再重新下载')
            else:
                self.save_img(album_img_url, photo_name)
'''


album_cover = AlbumCover()
album_cover.spider()