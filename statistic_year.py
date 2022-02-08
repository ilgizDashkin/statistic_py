import json
import re
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS
from datetime import timedelta, datetime
#поиск даты   
def search_date(str1):
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
         # print(k)
         return k
    if result_date:
      #   print(result_date[0])
        return result_date[0]

# вычисление количества дней с 1970г
def date_sec(str_date):
    delta=datetime.strptime(str_date, "%d.%m.%Y")-datetime.strptime("01.01.1970", "%d.%m.%Y")
   #  print(delta.days)     
    return delta.days

# чтоб мог прочитать нужно сохранять в json формате в программе PHPmyAdmin из опенсервера
#  с новым плагином json , в hostimane не создает валидный json и не забываем encoding='utf-8'
filname='table_49.json'
with open(filname, encoding='utf-8') as f:
    pop_data=json.load(f)
pop_data=pop_data[2]
# print(pop_data["data"])
pop_data=pop_data['data']


kl=[]
names=[]
name='name'
date='date'
dates='dates'
for pop_dict in pop_data: 
    povr={}
    povr[name]=pop_dict["COL 1"]
    # print(name)
    # povr[name]=pop_dict["COL 2"]
    k=pop_dict["COL 2"]
    # print("\n col2  {}".format(len(k)))
    # print(k)
    if len(k)>12:# нужно проверять если в строке дата в коротких нету
        k=search_date(k)
        povr[dates]=k
        povr[date]=date_sec(k)
    else:
       povr[date]=0
       povr[dates]=0
    kl.append(povr)
    names.append(povr[name])
# print("\n количество {}".format(len(names)))
unic_names=set(names)
# print("\nмножество {}".format(unic_names))
# print("\n количество уникальных {}".format(len(unic_names)))
unic_names=list(unic_names)    
# print("\n povr {}".format(kl))
# print("\n количество {}".format(len(kl)))

massiv=[]
name='name'
date='date'
dates='dates'
for name_kl in unic_names:
   povr_massiv={}
   date_mass=[]
   dates_mass=[]
   for povr_kl in kl:
      if povr_kl[name]==name_kl:
         dates_mass.append(povr_kl[dates])
         date_mass.append(povr_kl[date])
   # print("name {}".format(name_kl)) 
   # print("множество date {}".format(date_mass))
   povr_massiv[name]=name_kl
   povr_massiv[date]=date_mass
   povr_massiv[dates]=dates_mass
   massiv.append(povr_massiv)    
# print("\n massiv {}".format(massiv))   

def date_povr(massiv):
   """сортируем по годам по условию"""
   # year="01.01.2019"
   year="01.01."+years
   t=datetime.strptime(year, "%d.%m.%Y")-datetime.strptime("01.01.1970", "%d.%m.%Y")
   t=t.days
   massiv2=[]
   name='name'
   date='date'
   for kls in massiv:   
        povr_massiv={}
        kls_mass=[]
      # print("\n kls {}".format(kls)) 
        for kls_date in kls[date]:
          #  print("\n kls_date {}".format(kls_date)) 
            if kls_date>t and kls_date<t+365:
                kls_mass.append(kls_date)
        if len(kls_mass):#только даты больше нуля
            povr_massiv[name]=kls[name]
            povr_massiv[date]=kls_mass
            massiv2.append(povr_massiv)
   print("\n massiv2 {}".format(massiv2)) 
   print("\n massiv2 {}".format(len(massiv2)))
   return massiv2

year_mass=['1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']

names_kl, k_povr=[],[]
for year in year_mass:
    years=year
    new_a=date_povr(massiv)
    total_pov=0
    for x in new_a:
       pov_count=len(x[date])
       total_pov+=pov_count
    # print(year," повреждений  ", total_pov)
    names_kl.append(year)
    k_povr.append(total_pov)
print("\n year {}".format(names_kl)) 
print("\n kolich {}".format(k_povr)) 
# создание диаграммы
my_style=LS('#333366',base_style=LCS)
chart=pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)
chart.title='количество повреждений за 20 лет'
chart.x_labels=names_kl
chart.y_title="количество повреждений"
chart.add('',k_povr)
chart.render_to_file("povr_in_years.svg") 

