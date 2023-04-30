#!/usr/bin/python3
#coding:utf-8
from json import loads
from requests import post
from ast import literal_eval
from time import sleep

def PostApi(key):#Post Api
    ApiKey = '3975l6lr5pcbvidl6jl2'
    url = 'http://api.interpreter.caiyunai.com/v1/translator'
    date = {
            "source" : key, 
            "trans_type" : "auto2zh",
            "request_id" : "demo",
            "detect": True,
            }
    headers = {
            'content-type': "application/json",
            'x-authorization': "token " + ApiKey,
    }
    while True:
        ApiDate = post(url,date,headers)
    #print(ApiDate.text)
        if ApiDate.status_code == 200:
            return literal_eval(ApiDate.text)['tgt_text']
            break
        else
            time.sleep(5)
            
def TextSegment(DateKeys):#文本分段
    i = len(DateKeys)
    Keys = ''
    Dkeys = []
    for i in range(i):
        Keys = Keys + DateKeys[i].replace('\n','^C^') + '\n'
        if len(Keys) < 4500:
            Keys1 = Keys
        else :
            Keys = ''
            Keys = Keys + DateKeys[i].replace('\n','^C^') + '\n'
            Dkeys.append(Keys1.strip('\n'))
    return Dkeys

def ReadTransFile():#读取
    with open(f"{Path}\ManualTransFile.json",'r',encoding='utf-8') as ff:
        return loads(ff.read())

def WriteTransFile(json):#写入
    with open(f'{Path}\TrsData.json','w+',encoding='utf-8') as ff:
        ff.write(str(json))

def DealWithApiDate(Date):#处理数据
    DateKeys = list(Date.keys())
    text = ''
    DateKeysS = TextSegment(DateKeys)#分段以进行加速翻译避免QPS超标
    for i in range(len(DateKeysS)):
        print(f'[i]正在进行{len(DateKeysS)}个分段中的{i+1}')
        text = text + (PostApi(DateKeysS[i]))
    text = text.split('\n')
    for i in range(len(text)):
        Date[DateKeys[i]] = text[i].replace('^C^','\n')
    WriteTransFile(Date)
    print('[i]all ok')

if __name__ == '__main__' :
    Path = input('[in]请输入存在ManualTransFile.json的目录路径>>')
    DealWithApiDate(ReadTransFile())
