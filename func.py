import os
from tqdm import tqdm
from PIL import Image
from bs4 import BeautifulSoup
import requests
import urllib.request
import re


class Func():
    def ReplaceAll(self,repString):
        replaceDict = {
        'ı':'i',
        'ğ':'g',
        'ü':'u',
        'ş':'s',
        'ö':'o',
        'ç':'c',
        'İ':'I',
        'Ğ':'G',
        'Ü':'U',
        'Ö':'O',
        'Ç':'C',
        ' - ':'-',
        ' ':'-',
        '*':'-',
        '.':'-',
        ',':'-',
        '/':'-'
        }
        newStr = ''
        for c in repString:
            if replaceDict.get(c) != None:
                newStr = newStr + replaceDict[c]
            else:
                newStr = newStr + c
        return newStr
#-    
    def FolderControlCreate(self,folderName):
        if os.path.exists(folderName) == False:
            os.mkdir(folderName)
            print('Folder creating. ')    
        else:
            print('Folder created. ')       
#-  
    def SearchLink(self,source,hrefId,url):
        aTagArray = []              
        for aTag in tqdm(source.find_all("a"), "Products link are being scanned"):
            aTags = aTag.attrs.get("href")
            aTagFind = str(aTags).find(hrefId)
            
            if not aTags:
                continue
            else:
                if aTagFind != -1:
                        aTagArray.append(aTags)
        return aTagArray        
#-  
    def DownloadImg(self,aHref,findData,folders,url,inputValue):
            r = requests.get(aHref)
            source = BeautifulSoup(r.content,"html.parser")
            imgTypes = {
                'jpg' : 'jpg',
                'png' : 'png',
                'jpeg' : 'jpeg',
                'webp' : 'webp'
            }
            for img in tqdm(source.find_all("img"), "Pictures are being scanned"):                   
                imgUrl = img.attrs.get("src")
                if(str(imgUrl).find('http') == -1 | str(imgUrl).find('https') == -1):
                    imgUrl = url+imgUrl
                imgNameSplit = img.attrs.get("src").split('/')
                imgType = img.attrs.get("src").split('.')
                print(imgUrl)
                if not imgUrl:
                  continue
                else:
                  if(imgTypes.get(imgType[1]) and str(imgUrl).find(findData) != -1):                                              
                      imgName = folders+"/"+imgNameSplit[len(imgNameSplit)-1]
                      opener = urllib.request.URLopener()
                      opener.addheader('User-Agent', 'whatever')
                      opener.retrieve(imgUrl, imgName)
                      if inputValue.upper() == 'Y':
                          image = Image.open(imgName)
                          w, h = image.size
                          if int(w) >= 1100 or int(h) >= 1100:
                              w = w/4
                              h = h/4
                          else:
                              wif = w/2
                              hif = h/2 
                      
                              if wif >= 225 or hif >= 225:
                                  w = w/2
                                  h = h/2
                              else:
                                  w = w/3
                                  h = h/3
                          if w >= 225 or h >= 225:
                              new_image = image.resize((int(w), int(h))).convert("RGB")
                              new_image.save(imgName)
                  else:
                      continue              
#-  
    def DataMining(self,href,tags):
        repdict = {
            '<':'',
            "'":'',
            '"':'',
            '=':' ',
            '>':''
        }
        retunArray = []
        productTags = tags.split(',')
        r = requests.get(href)
        source = BeautifulSoup(r.content,"html.parser")
        for productTag in productTags:
            newStr = ''
            for ptg in productTag:
                if repdict.get(ptg) != None:
                    newStr = newStr + repdict[ptg]
                else:
                    newStr = newStr + ptg
                    
            newStr = newStr.split(' ')
            
            finds = source.find_all(newStr[0],attrs={newStr[1]:newStr[2]})
            if(len(finds) > 0):
                retunArray.append(finds[0])
        return retunArray
#-  
    def CreateHtmlInfo(self,title,infoArray,folder):
        html_cd = folder+"/index.html"
        if os.path.exists(html_cd) == False:
            readFolder = open(html_cd,"a", encoding='utf8')
            html_head = '<html><head><meta charset="utf-8" /><meta http-equiv="x-ua-compatible" content="ie=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>'+title+'</title></head><body>'
            writeFolder = html_head+''.join([str(elem) for elem in infoArray])+'</body></html>'
            readFolder.write(writeFolder)
            readFolder.close()
            return print("Index creating.")
        else:                
            return print("Index created.")


                    
             