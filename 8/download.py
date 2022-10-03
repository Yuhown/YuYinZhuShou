from urllib.request import urlretrieve
from urllib.parse import quote
import requests
import random
import json


musicName=input('请输入歌曲名称：')
encodName=quote(musicName)
#在浏览器开发者模式（F12）下获取url和referer地址
url='https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1'.format(encodName)
referer='https://www.kuwo.cn/search/list?key={}'.format(encodName)
# 请求头
headers = {
    "Cookie": "_ga=GA1.2.2021007609.1602479334;\
Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1602479334,1602673632; _gid=GA1.2.168402150.1602673633; \
Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602673824; kw_token=5LER5W4ZD1C",
    "csrf": "5LER5W4ZD1C",
    "Referer": "{}".format(referer),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
}
#发起get请求，返回一个请求成功后的响应对象
response=requests.get(url=url,headers=headers)
#获取响应对象字符串形式的页面数据并进行加载
dict2=json.loads(response.text)
misicInfo=dict2['data']['list']  # 歌曲信息的列表
musicNames=list()   # 歌曲名称的列表
rids=list()    # 存储歌曲rid的列表
for i in range(len(misicInfo)):
    name=misicInfo[i]['name']+'-'+misicInfo[i]['artist']
    musicNames.append(name)
    rids.append(misicInfo[i]['rid'])
    print('【{}】-{}->>>{}'.format(i+1,int(random.random()*10)*'#$',name))
# 下载歌曲
id=int(input('请输入歌曲序号:'))
musicRid=rids[id-1]
url2 = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=music&httpsStatus=1'.format(musicRid)
headers2={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
response2=requests.get(url=url2,headers=headers2)
dict3=json.loads(response2.text)
downloadUrl=dict3['data']['url']
urlretrieve(url=downloadUrl,filename='{}.mp3'.format(musicNames[id-1]))  
