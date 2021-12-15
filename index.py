# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import func
import json
import locale

with open("config.json", encoding='utf-8') as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

locale.setlocale(locale.LC_ALL, jsonObject['localeTimeZone'])

os.system("color b")
os.system("cls")

link_in = []
link_array = []
pro_array = []
img_array = []
print("#"*15+"-"*30+"#"*15)
print(" "*20+"Program Starting up"+" "*20)
print("#"*15+"-"*30+"#"*15)

time.sleep(1)
if(len(jsonObject) > 0):
    
    productsUrl = jsonObject['mainUrl'] + jsonObject['subPath']

    functionClass = func.Func()
    functionClass.FolderControlCreate(jsonObject['folderPath'])
    folderMainPath = jsonObject['folderPath']+"/"+functionClass.ReplaceAll(str(jsonObject['mainFolderName']).lower())
    functionClass.FolderControlCreate(folderMainPath)
    
    subDict = folderMainPath+"/"+functionClass.ReplaceAll(jsonObject['subFolderName'])
    functionClass.FolderControlCreate(subDict)
    #creat base folders
    r = requests.get(productsUrl)
    source = BeautifulSoup(r.content,"html.parser")
    #products link searching    
    print("#"*15+"-"*30+"#"*15)
    print(" "*17+"Info is gathering & saving"+" "*17)
    print("#"*15+"-"*30+"#"*15)
    aTagArray = functionClass.SearchLink(source,jsonObject['aHrefId'],jsonObject['mainUrl'])
    print("Number of products : "+str(len(aTagArray)))
    print(r"Do yout want to image auto resizing?(Y\N)")
    userInput = input()
    endNbr = 1
    
    for ahref in aTagArray:
       newUrl = jsonObject['mainUrl']+ahref 
       dataResponse = functionClass.DataMining(newUrl,str(jsonObject['infoTags']))
       title = ahref.replace(jsonObject['aHrefId'], '') 
       titleUrl = functionClass.ReplaceAll(title)
       productFolder = subDict+"/"+titleUrl
       print(str(endNbr)+"/"+str(len(aTagArray))+" : "+ title)
       functionClass.FolderControlCreate(productFolder)
       functionClass.CreateHtmlInfo(title,dataResponse,productFolder)
       functionClass.DownloadImg(newUrl,jsonObject['imgGeneralPath'],productFolder,jsonObject['mainUrl'],userInput)
       endNbr = endNbr + 1  
       print("-"*60)
    print("Process completed. Edit the link and subcategory of the other page in config.json.")        
else:
    print("Fill in the index file.")
    quit

        
    
#Linkler ayrılıyor
#Linklere girip ürünlere klasör açarak indirme işlemi kaldı    
