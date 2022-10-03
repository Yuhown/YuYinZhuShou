# -*- coding:utf-8 -*-
import requests
import bs4


def get_web(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59"}
    res = requests.get(url, headers=header, timeout=5)
    # print(res.encoding)
    content = res.text.encode('ISO-8859-1')# 进行编码
    return content# 返回编码后的内容


def parse_content(content):
    soup = bs4.BeautifulSoup(content, 'html.parser') # 初始化

    #存放天气情况
    list_weather = []
    weather_list = soup.find_all('p', class_='wea')
    for i in weather_list:
        list_weather.append(i.text)

    # 存放日期
    list_day = []
    i = 0
    day_list = soup.find_all('h1')# 获取所有h1标签下的内容
    for each in day_list: # 找到前7个h1，并保存在列表中
        if i <= 6:
            list_day.append(each.text.strip())
            i += 1
    # print(list_day)

    #存放温度：最高温度和最低温度
    tem_list = soup.find_all('p', class_='tem')
    i = 0
    list_tem = []
    for each in tem_list:
        if i == 0:
            list_tem.append(each.i.text)
            i += 1
        elif i > 0:
            list_tem.append([each.span.text, each.i.text])
            i += 1
    # print(list_tem)

    #存放风力
    list_wind = []
    wind_list = soup.find_all('p', class_='win')
    for each in wind_list:
        list_wind.append(each.i.text.strip())
    # print(list_wind)
    return list_day, list_weather, list_tem, list_wind


def get_content(url):
    content = get_web(url)# 获取网页内容
    day, weather, tem, wind = parse_content(content)# 获取信息
    item = 0
    with open('weather.txt', 'w', encoding='utf-8') as file:
        for i in range(0, 7):
            if item == 0:
                file.write(day[i]+':\t')
                file.write(weather[i]+'\t')
                file.write("今日气温："+tem[i]+'\t')
                file.write("风力："+wind[i]+'\t')
                file.write('\n')
                item += 1
            elif item > 0:
                file.write(day[i]+':\t')
                file.write(weather[i] + '\t')
                file.write("最高气温："+tem[i][0]+'\t')
                file.write("最低气温："+tem[i][1] + '\t')
                file.write("风力："+wind[i]+'\t')
                file.write('\n')
def report():
    url = "http://www.weather.com.cn/weather/101020100.shtml"
    print("正在爬取数据...........................")
    get_content(url)
    print("爬取完毕！！")
    with open('weather.txt',mode='r',encoding='utf-8') as f:
        data = f.readlines()
        #print(data[0])
        return data[0]

if __name__ == "__main__":
##    #url = "http://www.weather.com.cn/weather/101010100.shtml"
##    url = "http://www.weather.com.cn/weather/101020100.shtml"
##    print("正在爬取数据...........................")
##    get_content(url)
##    print("爬取完毕！！")
##    with open('weather.txt',mode='r',encoding='utf-8') as f:
##        data = f.readlines()
##        for i in range(0, 7):
##            print(data[i])
    report()
 

 
 



