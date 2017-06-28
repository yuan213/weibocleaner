# -*- coding: utf-8 -*-
import requests
import json
import lxml
from bs4 import BeautifulSoup
import time
import random
import re

s=requests.session()
s1=requests.session()
global st
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
        'Connection' : 'keep-alive',}

def login(username,pwd):
  url = 'https://passport.weibo.cn/sso/login'
  submit_data = {'username':username,'password':pwd,
  'savestate':'1','r':'http://weibo.cn/','ec':'0',
  'pagerefer':'','entry':'mweibo','wentry':'',
  'loginfrom':'','client_id':'','code':'',
  'qq':'','mainpageflag':'1','hff':'','hfp':'',}

  #模拟登陆
  req1 = s.post(url=url,data=submit_data, headers=headers,timeout=10)
  js1 = json.loads(req1.text)
  resultCode=js1['retcode']
  if resultCode == 20000000:
    print('恭喜，登陆成功!')
  data1=js1['data']
  uid=data1['uid']
  return uid

def idlist(uid):
  profileurl='https://weibo.cn/'+uid+'/profile'+'?page=1'
  req2=s.get(url=profileurl,headers=headers,timeout=10).content
  soup=BeautifulSoup(req2, "lxml")
     #获取博文总页数
  soup1=soup.find_all('input',{'name':'mp'})
  value=int(soup1[0].attrs['value'])
  soup9=soup.find_all('form',{'method':'post'})
    #获得st值
  sturl=soup9[0].attrs['action']
  global st
  st=sturl.split('=')[1]

  containerid = '107603'+uid
  idlist2=[]

  for num in range(1,value+1):
      idurl='https://m.weibo.cn/api/container/getIndex?type=uid&value='+uid+'&containerid='+containerid+'&page='+str(num)
      req3=s1.get(url=idurl,headers=headers,timeout=20)
      
      js2 = json.loads(req3.content)
      length=len(js2["cards"])
      if length!=10:      
           print('正在获取第'+str(num)+'页的微博id','本页有微博'+str(length)+'条')
      for num1 in range(0,length):
          idlist2.append(js2["cards"][num1]["mblog"]["bid"])
          
  print('微博获取完毕')

  return idlist2
def dellist(idlist):

 for idid in idlist:
    timea=random.uniform(3,8)
    time.sleep(timea)
    url1='https://weibo.cn/mblog/del?type=del&id='+idid+'&act=delc&rl=1&st='+st
    req4=s.get(url=url1,headers=headers,timeout=20)

      
username=input('请输入微博用户名:')
pwd=input('请输入微博密码:')
uid=login(username,pwd)
idlista=idlist(uid)
dellist(idlista)

