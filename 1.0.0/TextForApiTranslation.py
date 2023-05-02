#!/usr/bin/python3
#coding:utf-8
from json import loads
import requests
import json
from ast import literal_eval
from time import sleep


def PostApi(key):#Post Api
    ApiKey = '3975l6lr5pcbvidl6jl2'
    url = 'http://api.interpreter.caiyunai.com/v1/translator'
    payload = {
            "source" : key, 
            "trans_type" : "auto2zh",
            "request_id" : "demo",
            "detect": True
            }
    headers = {
            'content-type': "application/json",
            'x-authorization': "token 3975l6lr5pcbvidl6jl2"
    }
    while True:
        ApiDate = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        if ApiDate.status_code == 200:
            print(json.loads(ApiDate.text)["target"])
            return json.loads(ApiDate.text)["target"]
            break
        else :
            sleep(5)

def TextSegment(DateKeys):#文本分段
    i = len(DateKeys)#获取待翻译文本元素数
    start = 0
    Keys = ''
    fen_duan = {}
    
    for i in range(i):
        Keys = Keys + DateKeys[i] 
        if len(Keys) < 3500:
            Keys1 = Keys
        else :
            fen_duan[start] = i
            Keys = ''
            start = i
            
    fen_duan[start] = i 
    print(fen_duan)
    
    return fen_duan

def ReadTransFile():#读取
    with open(f"{Path}\ManualTransFile.json",'r',encoding='utf-8') as ff:
        return loads(ff.read())

def WriteTransFile(json):#写入
    with open(f'{Path}\TrsData.json','w+',encoding='utf-8') as ff:
        ff.write(str(json))

def DealWithApiDate(Date):#处理数据
    DateKeys = list(Date.keys())
    text = []
    fen_duan = TextSegment(DateKeys)#分段字典
    for i in range(len(fen_duan)):
        print(f'[i]正在进行{len(fen_duan)}个分段中的{i+1}')
        stat = list(fen_duan)[i]
        end  = fen_duan[stat]
        text += (PostApi(DateKeys[stat:end]))
    for i in range(len(text)):
        Date[DateKeys[i]] = text[i]
    WriteTransFile(json.dumps(Date,ensure_ascii=False))
    print('[i]all ok')

if __name__ == '__main__' :
    Path = input('[in]请输入存在ManualTransFile.json的目录路径>>')
    DealWithApiDate(ReadTransFile())
