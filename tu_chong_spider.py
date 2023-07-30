# -*- coding: utf-8 -*-
import os
import requests
import random
import json
from lxml import etree
import time
import sys
 

import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
def url_list():
    ullist =[]
    tag_name = '游戏'
    for num in range(1,5):
        start_url = 'http://tuchong.com/rest/tags/' + tag_name + '/posts?page={}&count=20&order=weekly'.format(num)
        ullist.append(start_url)
    return ullist
def choie_header():
    agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',]
    agent = random.choice(agent_list)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'tuchong.com',
        'Referer': 'https://tuchong.com/explore/',
        'User-Agent': agent
    }
    return headers

def get_content(ullist):
    # print(ullist)
    img_url_list = []
    for url_tu in ullist:
        print("正在访问：",url_tu)
        time.sleep(1)
        url_response = requests.get(url_tu).content.decode("utf-8")

        picture = json.loads(url_response)["postList"]
        #列表遍历提取
        for mv_url in picture:
            # picture["postList"]
            content_url = mv_url["url"]
            # biaoti = mv_url["title"] if len(mv_url["title"]) > 0 else "NO_TITLE"
            page_num = mv_url["image_count"]
            if page_num > 0:
            # print(content_url,biaoti,page_num)
                img_url_list.append(content_url)
    return img_url_list

def run(get_content_list):
    for img_url in get_content_list:
        time.sleep(1)
        response_str = requests.get(img_url).content.decode("utf-8")
        # print(response_str,"*"*100)
        content_url_str = etree.HTML(response_str)
        xpath_content = content_url_str.xpath("//article[@class='post-content']/img")
        title_name = content_url_str.xpath("//h1[@class='post-title']/text()")
        if len(title_name) > 0:
            title_name = content_url_str.xpath("//h1[@class='post-title']/text()")[0].replace("?", " ").replace("′","").replace("\\"," ").replace("/"," ").replace("\""," ").replace(":"," ").replace("*"," ").replace("<"," ").replace(">"," ").replace("|","")
        else:
            title_name = "name_less"
        #根据window系统 文件夹 不能 包含特殊字符
        # title_name.replace("\\", " ").replace("/", " ").replace("\"", " ").replace(":", " ").replace("*", " ").replace("<"," ").replace(">", " ").replace("|", "")
        # img_num = content_url_str.xpath("//span[@class='theater-indicator']/text()")
        # 创建文件夹
        num_len = len(xpath_content)
        folder_path = '/Users/luzhaoyang/Desktop/测试/' + title_name + str(num_len) + "p" + '/'

        if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
            os.makedirs(folder_path)  # 创建文件夹
        for img in xpath_content:
            item = {}
            item["id"] = img.xpath("./@id")[0]
            item["src"] = img.xpath("./@src")[0]
            img_name = folder_path + title_name + item["id"] + '.png'
            # print(item["id"], item["src"])
            response = requests.get(item["src"]).content
            with open(img_name, 'wb') as file:
                file.write(response)
                # print("正在下载：%s 编号：%s 下载完成" % (title_name, item["id"]))
        print("下载完成：文件名- %s" % title_name )

if __name__ == '__main__':

    url_list = url_list()
    header_str = choie_header()
    get_content_list = get_content(url_list)
    run(get_content_list)