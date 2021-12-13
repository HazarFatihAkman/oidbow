# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import requests
import time
import numpy as np

import func

os.system("color b")
os.system("cls")

link_in = []
link_array = []
pro_array = []
img_array = []
print("#"*15+"-"*30+"#"*15)
print(" "*20+"Program Starting up"+" "*20)
print("#"*15+"-"*30+"#"*15)

readf = open("index.txt","r", encoding='utf8')
datam = readf.read().split('\n')
readf.close()

time.sleep(1)
if(len(datam) > 0):
    onurl = datam[0]
    link = datam[1]
    mainfol = datam[2]
    mainaddfol = datam[3]
    ahrefid = datam[4]
    protag = str(datam[5])
    stok = datam[6]
    imgid = datam[7]

    funct = func.Func()

    funct.foldercontcre("Folders")
    maindict = "Folders/"+funct.replaceAll(mainfol)
    funct.foldercontcre(maindict)
    mainadict = maindict+"/"+funct.replaceAll(mainaddfol)
    funct.foldercontcre(mainadict)
    #creat base folders

    r = requests.get(link)
    source = BeautifulSoup(r.content,"html.parser")
    #products link searching    
    print("#"*15+"-"*30+"#"*15)
    print(" "*17+"Info is gathering & saving"+" "*17)
    print("#"*15+"-"*30+"#"*15)
    aharray = funct.searchlink(source,ahrefid,onurl)   
    print("Number of products : "+str(len(aharray)))

    print(r"Do yout want to image auto resizing?(Y\N)")
    user_in = input()
    end_nmbr = 1
    for ahref in aharray:
        data_turn = funct.datamining(ahref,protag,stok,mainadict)
        title_link = funct.replaceAll(data_turn[0])
        pro_folder = mainadict+"/"+title_link
        print(str(end_nmbr)+"/"+str(len(aharray))+" : "+data_turn[0])
        funct.foldercontcre(pro_folder)
        funct.creathtmlInfo(data_turn,pro_folder)
        funct.downloadimg(ahref,imgid,pro_folder,onurl,user_in)
        end_nmbr = end_nmbr + 1  
        print("-"*60)

    print("Process completed. Edit the link and subcategory of the other page in index.txt.")        
else:
    print("Fill in the index file.")
    quit

        
    
#Linkler ayrılıyor
#Linklere girip ürünlere klasör açarak indirme işlemi kaldı    
