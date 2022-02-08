import json
import re
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

# чтоб мог прочитать нужно сохранять в json формате в программе PHPmyAdmin из опенсервера
#  с новым плагином json , в hostimane не создает валидный json и не забываем encoding='utf-8'
filname='table_49.json'
with open(filname, encoding='utf-8') as f:
    pop_data=json.load(f)
pop_data=pop_data[2]
# print(pop_data[1])
pop_data=pop_data['data']
names=[]
for pop_dict in pop_data: 
    name=pop_dict["COL 1"]
    # print(name)
    names.append(name)
# print("\n количество {}".format(len(names)))
unic_names=set(names)
# print("множество {}".format(unic_names))
# print("\n количество уникальных {}".format(len(unic_names)))
unic_names=list(unic_names)
# print("уникальные имена {}".format(unic_names))
print("\n количество уникальных {}".format(len(unic_names)))
# n=0
kl={}
for name_kl in unic_names: 
    k=names.count(name_kl)
    # print("kl  {}".format(name_kl))
    # print("количество  {}\n".format(k))
    # n+=1
    # print("N= {}".format(n))
    kl[name_kl]=k
# print("kls  {}\n".format(kl))


def sort_dictionary_by_value(dictionary):
    """сортировка словаря по значению"""
    list_of_sorted_pairs = [(k, dictionary[k]) for k in sorted(dictionary.keys(), key=dictionary.get, reverse=True)]
    # Так мы создаём кортежи (ключ, значение) из отсортированных элементов по ключу равному "значение ключа"
    # Также отсортированы будут и ключи, имеющие одно значение
    # "reverse = False" говорит, что перебор нужно делать в обычном порядке
    # Если нужно отсортировать значения в обратном порядке, то reverse можно сделать = True
    return list_of_sorted_pairs # после сделанных операций возвращаем получившийся список

new_a = sort_dictionary_by_value(kl)

names_kl, k_povr=[],[]
for x in new_a:
    if x[1]>30:
        print(x[0]," совпадений  ", x[1])
        names_kl.append(x[0])
        k_povr.append(x[1])
    # if x[1]>30 and x[1]<=40:
    #     print(x[0]," совпадений  ", x[1])
    #     names_kl.append(x[0])
    #     k_povr.append(x[1])
    # if x[1]>20 and x[1]<=30:
    #     print(x[0]," совпадений  ", x[1])
    #     names_kl.append(x[0])
    #     k_povr.append(x[1])
    # if x[1]>10 and x[1]<=20:
    #     # print(x[0]," совпадений  ", x[1])
    #     names_kl.append(x[0])
    #     k_povr.append(x[1])
    # if x[1]>5 and x[1]<=10:
    #     # print(x[0]," совпадений  ", x[1])
    #     names_kl.append(x[0])
    #     k_povr.append(x[1])
    # if x[1]<=5: 
    #     # print(x[0]," совпадений  ", x[1])
    #     names_kl.append(x[0])
    #     k_povr.append(x[1])
print("\n количество povr {}".format(len(k_povr)))
# создание диаграммы
my_style=LS('#333366',base_style=LCS)
chart=pygal.Bar(style=my_style,x_label_rotation=45,show_legend=False)
chart.title='самые уставшие КЛ до 01.2022'
chart.x_labels=names_kl
chart.y_title="количество повреждений"
chart.add('',k_povr)
chart.render_to_file("populars.svg")