import json
import re
import numpy as np
import pandas as pd
import sklearn 
import matplotlib
from matplotlib import pyplot as plt
from datetime import timedelta, datetime
from sklearn.linear_model import LinearRegression #важно явно импортировать
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS
import time
from collections import Counter 
import math
# import geocoder
from time import sleep

filname='table_44.json'
with open(filname, encoding='utf-8') as f:
    pop_data=json.load(f)
pop_data=pop_data[2]
# print(pop_data["data"])
pop_data=pop_data['data']
# print(pop_data)
# data_pandas=pd.DataFrame(pop_data)#создаю панда дата фрэйм 
# display(data_pandas[:5])
# data_pandas.info()

# убираем из адресов слова дома жд итд
def adress_name(adr):
      adr=str(adr)  
      if adr.find('ж/д')!=-1:
         res_adr=adr.replace('ж/д','ул.')
         return ('"уфа '+res_adr+'",')
      if adr.find('ч/д')!=-1:
         res_adr=adr.replace('ч/д','ул.')
         return ('"уфа '+res_adr+'",')
      if adr.find('дома')!=-1:
         res_adr=adr.replace('дома','ул.')
         return ('"уфа '+res_adr+'",')
      if adr.find('д.')!=-1:
         res_adr=adr.replace('д.','ул.')
         return ('"уфа '+res_adr+'",')
      else:
         res_adr=adr
         return ('"уфа '+res_adr+'",')


#поиск адресов 
def adress(str_adress):
   str_adress=str_adress.lower()
   patterns=['ул\. [0-9а-яёА-ЯЁ]{3,}-[0-9а-яёА-ЯЁ]{3,}',
   'ул\. [0-9а-яёА-ЯЁ]{3,} \d+/\d+',
   'ул\. [0-9а-яёА-ЯЁ]{3,}, \d+/\d+',
   'ул\. [0-9а-яёА-ЯЁ]{3,} \d+',
   'ул\.[0-9а-яёА-ЯЁ]{3,}, \d+/\d+',
   'ул\.[0-9а-яёА-ЯЁ]{3,} \d+',
   'ул\. [0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',
   'ул\.[0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',
   'ул\. [0-9а-яёА-ЯЁ]{3,}\-\d+',
   'ул\.[0-9а-яёА-ЯЁ]{3,}\-\d+',

   # 'д [а-яёА-ЯЁ]{3,} \d+/\d+',

   'д\. [0-9а-яёА-ЯЁ]{3,} \d+/\d+',
   'д\. [0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',  
   'д\.[0-9а-яёА-ЯЁ]{3,}\-\d+',
   'д\.[0-9а-яёА-ЯЁ]{3,} \d+',
   'дома [0-9а-яёА-ЯЁ]{3,} \d+/\d+',
   'дома [0-9а-яёА-ЯЁ]{3,} \d+',
   'дома [0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',
   'дома [0-9а-яёА-ЯЁ]{3,}\-\d+',
   'ч/д [0-9а-яёА-ЯЁ]{3,}, \d+/\d+',
   'ч/д [0-9а-яёА-ЯЁ]{3,}, \d+',
   'ч/д [0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',
   'ч/д [0-9а-яёА-ЯЁ]{3,}\-\d+',  
   'ж/д [0-9а-яёА-ЯЁ]{3,}, \d+/\d+',
   'ж/д [0-9а-яёА-ЯЁ]{3,},\d+/\d+',
   'ж/д [0-9а-яёА-ЯЁ]{3,},\d+',
   'ж/д [0-9а-яёА-ЯЁ]{3,}, \d+',
   'ж/д [0-9а-яёА-ЯЁ]{3,}\-\d+/\d+',
   'ж/д [0-9а-яёА-ЯЁ]{3,}\-\d+'
   ]
   for pattern in patterns:
      all_words=re.findall(pattern,str_adress)
      if all_words:
         # all_words=all_words[0]
         # all_words=adress_name(all_words)
         # print(all_words)
         return all_words

#поиск фидеров 
def name_fider(str_adress):
   str_adress=str_adress.lower()
   patterns=['ф-\d+[а-яёА-ЯЁ]{0,1}-\d+[а-яёА-ЯЁ]{0,1}']
   for pattern in patterns:
      all_words=re.findall(pattern,str_adress)
      if all_words:
         # all_words=all_words[0]
         # all_words=adress_name(all_words)
         # print(all_words)
         return all_words
      else:
         return 'rp_tp'
# k=name_fider('ф-4д-101')
# print(k)

#поиск пс 
def name_ps(str_adress):
   str_adress=str_adress.lower()
   patterns=['ф-\d+[а-яёА-ЯЁ]{0,1}']
   for pattern in patterns:
      all_words=re.findall(pattern,str_adress)
      if all_words:
         if len(re.findall('[а-яёА-ЯЁ]',all_words[0]))>1:
            return 'тэц-2'
         else:
            return all_words[0]#int(re.findall('\d+',all_words[0])[0])
      else:
         return 'рп-тп'
# k=name_ps('ф-4-101')
# print(k)

#поиск № пс 
def number_ps(str_adress):
   str_adress=str_adress.lower()
   patterns=['ф-\d+[а-яёА-ЯЁ]{0,1}']
   for pattern in patterns:
      all_words=re.findall(pattern,str_adress)
      if all_words:
         if len(re.findall('[а-яёА-ЯЁ]',all_words[0]))>1:
            return 'tec'
         else:
            return re.findall('\d+',all_words[0])[0]
      else:
         return 'rp_tp'

#поиск даты   
def search_date(str1):
    if len(str1)>10:    
        result_date=re.search(r'([0-2]\d|3[01])\.(0\d|1[012])\.(\d{4})', str1)
        if result_date==None:
         result_date=re.search(r'((\d{1,2} января)|(\d{1,2} февраля)|(\d{1,2} марта)|(\d{1,2} апреля)|(\d{1,2} мая)|(\d{1,2} июня)|(\d{1,2} июля)|(\d{1,2} августа)|(\d{1,2} сентября)|(\d{1,2} октября)|(\d{1,2} ноября)|(\d{1,2} декабря)) (\d{4})', str1)
         result_date1=re.search(r'(\d{1,2} января) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" января ", ".01.")
         result_date1=re.search(r'(\d{1,2} февраля) (\d{4})', result_date[0])
         if result_date1:
               k=result_date[0].replace(" февраля ", ".02.")
         result_date1=re.search(r'(\d{1,2} марта) (\d{4})', result_date[0])
         if result_date1:
               k=result_date[0].replace(" марта ", ".03.")
         result_date1=re.search(r'(\d{1,2} апреля) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" апреля ", ".04.")
         result_date1=re.search(r'(\d{1,2} мая) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" мая ", ".05.")
         result_date1=re.search(r'(\d{1,2} июня) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" июня ", ".06.")
         result_date1=re.search(r'(\d{1,2} июля) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" июля ", ".07.")
         result_date1=re.search(r'(\d{1,2} августа) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" августа ", ".08.")
         result_date1=re.search(r'(\d{1,2} сентября) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" сентября ", ".09.")
         result_date1=re.search(r'(\d{1,2} октября) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" октября ", ".10.")
         result_date1=re.search(r'(\d{1,2} ноября) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" ноября ", ".11.")
         result_date1=re.search(r'(\d{1,2} декабря) (\d{4})', result_date[0])
         if result_date1:
            k=result_date[0].replace(" декабря ", ".12.")
        #  print(k)
         return k
        if result_date:
            # print(result_date[0])
            return result_date[0]

# вычисление количества дней с 1970г
def date_sec(str_date):
    delta=datetime.strptime(str_date, "%d.%m.%Y")-datetime.strptime("01.01.1970", "%d.%m.%Y")
    # print(delta)
    d=int(delta.days)*24*3600
    if d>3786912000: #пришлось мудрить чтоб избавится от 2099г отнял 100лет
       d=d-36500
       return delta.days-36500    
    return delta.days

def sec_month(sec):
   if sec>0:
      readable = time.gmtime(sec)
      return time.strftime("%m", readable)

def sec_year(sec):
   if sec>0:
      readable = time.gmtime(sec)
      return time.strftime("%Y", readable)

def sec_week(sec):
   if sec>0:
      readable = time.gmtime(sec)
      return time.strftime("%w", readable)

def sec_unix_time(sec):
   if sec>0:
      readable = time.gmtime(sec)
      return time.strftime("%Y-%m-%d", readable)

def sec_weeks(sec):
   if sec>0:
      readable = time.gmtime(sec)
      return time.strftime("%W", readable)

def search_zamer(str1):
    result=re.search(r'\d+ м от', str1)
    if result==None:
        result=re.search(r'\d+м от', str1)
    if result==None:
        result=re.search(r'\d+м. от', str1)
    if result==None:
        result=re.search(r'\d+м.от', str1)
    if result==None:
        result=re.search(r'\d+ м от', str1)
    if result==None:
        result=re.search(r'\d+м от', str1)
    if result==None:
        result=re.search(r'\d+м. от', str1)
    if result==None:
        result=re.search(r'\d+ м. от', str1)  
    if result==None:
        result=re.search(r'\d+ м от от', str1)
    if result==None:
        result=re.search(r'\d+ мот', str1)
    if result==None:
        result=re.search(r'\d+мот', str1)
    if result==None:
        result=re.search(r'\d+ м.от', str1) 
    if result==None:
        result=re.search(r'Концевая муфта', str1)
        result='0'                   
    if result:
    #   print("совпадение найдено "+result[0])
      zamer=re.search(r'\d+', result[0])
      return (int(zamer[0]))

# вся длина
def all_lenght(str1):
    result=re.search(r'вся длинна: \d+м', str1)
    if result:
    #   print(result[0])
      lenght=re.search(r'\d+', result[0])    
      return (int(lenght[0]))

# готовлю данные для пандас
dates_pov=[]
for priv in pop_data:
   date_pov={}
   # date_pov['id']=priv['id']
   date_pov['name']=priv['COL 1']
   date=search_date(priv['COL 2'])
   date_pov['zamer']=search_zamer(priv['COL 2'])
   date_pov['lenght']=all_lenght(priv['COL 2'])
   if date==None:
     #   print("нет даты  "+priv['id']+"  "+priv['COL 1']+"  "+priv['COL 2'])
     date_pov['date']="01.01.1970"
   elif date=='05.04.0128':
     date_pov['date']="05.04.1998" 
   else:
     #   print(date)
     date_pov['date']=date
   date_pov['date_sec']=date_sec(date_pov['date'])*24*3600
   date_pov['date_month']=sec_month(date_pov['date_sec'])
   date_pov['date_year']=sec_year(date_pov['date_sec']) 
   date_pov['date_unix']=sec_unix_time(date_pov['date_sec'])
   date_pov['date_week']=sec_week(date_pov['date_sec'])
   date_pov['date_weeks']=sec_weeks(date_pov['date_sec'])
   date_pov['priv']=priv['COL 2']
   if name_fider(priv['COL 1'])!=None:
     date_pov['name_f']=name_fider(priv['COL 1'])[0]
   if name_ps(priv['COL 1'])!=None:
     date_pov['name_ps']=name_ps(priv['COL 1'])
   if name_ps(priv['COL 1'])!=None:
     date_pov['number_ps']=number_ps(priv['COL 1'])
   # date_pov['name_f']=name_fider(priv['COL 1'])
   if adress(priv['COL 2'])!=None:
      date_pov['adress']=adress_name(adress(priv['COL 2'])[0])
    #   date_pov['latlng']=my_geocoder(date_pov['adress'])
   dates_pov.append(date_pov)
# print(dates_pov)

data_pandas=pd.DataFrame(dates_pov)#создаю панда дата фрэйм
data_pandas.head()
data_pandas.info()



# сводная таблица
pvt = data_pandas.pivot_table(index=['date_month'], columns=['date_year'], values='name', aggfunc='count')
# print(pvt)
# pvt.head()
# pvt.index
# pvt[['2019']]
# type(pvt)
# # среднее мода медиана в строке
# print(pvt.loc['01'].mean())
# print(pvt.loc['01'].mode())
# print(pvt.loc['01'].median())
# # print(pvt.loc['05', ['2017', '2018', '2019']])
# pvt.plot(figsize=(20, 10))
pvt.to_html('svod_tab.html')