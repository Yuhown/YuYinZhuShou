from aip import AipSpeech
import json
import requests
import wave
import numpy as np
import time
import webbrowser
import time
import pygame
import os
import urllib
from selenium import webdriver
import re
  
"""下载音乐"""
def get_music_url(name):
    driver.get('https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w='+name)
    driver.implicitly_wait(10)
    data = driver.find_element_by_xpath('//div[@class="songlist__item"]//a').get_attribute('href')
    data = {'mid' : data}
    print("data",data)
    return data

def get_music(data):
    req = requests.post('http://www.douqq.com/qqmusic/qqapi.php',data=data).content
    req = json.loads(req.decode('utf-8'))
    #req = json.loads(req.decode('unicode'))
    req = req.replace('\/','/')
    g = re.compile('"m4a":"(.*?)",')
    c = re.findall(g,req)
    c = c[0]
    return c

def save_music(c,name):
    os.makedirs('/music/',exist_ok=True)
    file_name = "%s.mp3" %name
    #file_path = os.path.join("/home/pi/Desktop/qq_music", file_name)  # only stitch English song's name
    file_path = "/music/" + file_name
    #file_path = file_path.decode('unicode')
    print("file_path",file_path)
    try:
        #urllib.request.urlretrieve( c , '/home/pi/Desktop/qq_music/' + name + '.mp3')
        urllib.request.urlretrieve( c , file_path)
    except:
        print("can't save the music")
        traceback.print_exc()

def DownloadMusic(name):
    try:
        data = get_music_url(name)
        c = get_music(data)
        save_music(c,name)
        return 1
    except:
        return 0          
    

