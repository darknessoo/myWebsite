#! encoding=utf-8
# @Time    : 2018/5/5 10:17
# @Author  : lhy

HIGH_ANONYMITY_PROXY_URL = 'http://www.xicidaili.com/nn/'
# TEST_IP_URL = 'http://www.whatismyip.com.tw/'
TEST_IP_URL_HTTP = 'http://2017.ip138.com/ic.asp'
TEST_IP_URL_HTTPS = 'http://2017.ip138.com/ic.asp'
HTTP_FILE_PATH = ''
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
basic_headers = {}
basic_headers['User-Agent'] = User_Agent
HTTPS_FILE_PATH = ''

import BeautifulSoup as bf, re, requests, traceback, time, socket


def get_ips():
    ips = []
    for i in range(1,2):
        url = HIGH_ANONYMITY_PROXY_URL+str(i)
        headers = basic_headers
        res = requests.get(url, headers=headers).content
        pattern = re.compile("^[\.0-9]+$")

        soup = bf.BeautifulSoup(res)
        ip_table = soup.find('table',id='ip_list')
        if ip_table:
            for tr in ip_table.findAll('tr'):
                tds = tr.findAll('td', limit=6)
                if len(tds) >= 2:
                    ip = str(tds[1].string)
                    port = str(tds[2].string)
                    addr = str(tds[3].string)
                    type = str(tds[5].string)
                    if pattern.match(ip):
                        ips.append({'ip':ip, 'port':port, 'addr':addr, 'type':type})
    return ips

def test_ip(ips=None):
    host_ip = get_pub_ip()
    print '本机ip为：{}'.format(host_ip)
    for ip in ips:
        proxy_ip = get_pub_ip(ip)
        if proxy_ip and proxy_ip != host_ip:
            print '代理成功，代理类型为{}，代理地址为{}:{}，代理ip为：{}'.format(ip['type'], ip['ip'], ip['port'], proxy_ip)


def get_pub_ip(test_ip = None):
    ip = None
    proxies = None
    url = TEST_IP_URL_HTTP

    if test_ip:
        #proxies 前面类型必须小写,当url为https时，用https代理，URL为http，用http代理
        proxies = {test_ip['type'].lower(): test_ip['ip'] + ':' + test_ip['port']}
        if test_ip['type'].lower() == 'https':
            url = TEST_IP_URL_HTTPS
        elif test_ip['type'].lower() == 'http':
            pass
        else:
            print 'ip 类型错误'
            return ip

    pattern = re.compile("\[([0-9]+?(?:\.[0-9]+?){3})\]")
    try:
        content = requests.get(url, proxies=proxies, timeout=5, headers=basic_headers).content
        soup = bf.BeautifulSoup(content)
        text = str(soup.find('center').string)
        search = pattern.search(text)
        if search:
            ip = search.group(1)
    except:
        # print traceback.print_exc()
        # print '代理类型为{}, 测试ip为：{},'.format(test_ip['type'], test_ip['ip'] + ':' + test_ip['port']) + '超时'
        pass
    finally:
        return ip

# test_ip(get_ips())


def taobao_spider():
    url = 'https://www.taobao.com/'
    print requests.get(url).content


#coding=utf-8
import re
import requests

url = 'https://s.taobao.com/search'
payload = {'q': 'python','s': '1','ie':'utf8'}  #字典传递url参数
with open('taobao_test.txt','w') as file:
    for k in range(0,100):        #100次，就是100个页的商品数据
        payload ['s'] = 44*k+1   #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推
        resp = requests.get(url, params = payload)
        print(resp.encoding)
        print(resp.url)          #打印访问的网址
        resp.encoding = 'utf-8'  #设置编码
        title = re.findall(r'"raw_title":"([^"]+)"',resp.text,re.I)  #正则保存所有raw_title的内容，这个是书名，下面是价格，地址
        price = re.findall(r'"view_price":"([^"]+)"',resp.text,re.I)
        loc = re.findall(r'"item_loc":"([^"]+)"',resp.text,re.I)
        x = len(title)           #每一页商品的数量

        for i in range(0,x) :    #把列表的数据保存到文件中
            text = unicode(k*44+i+1)
            text += u'书名：'
            text += title[i]
            text += '\n'+u'价格：'
            text += price[i]
            text += '\n'+u'地址：'
            text += loc[i]
            text += '\n\n'
            file.write(text.encode('utf-8'))