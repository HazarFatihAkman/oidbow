import os
from tqdm import tqdm
from PIL import Image
from bs4 import BeautifulSoup
import requests
import urllib.request
import re


class Func():
    def replaceAll(self,repstring):
        replacedict = {
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
        '/':'-',
        'ÄŸ':'g',
        'Ä±':'i',
        'ÅŸ':'s',
        'Ãœ':'U',
        'Ã¼':'u',
        'Ã¶':'o',
        'Ã§':'c',
        'Ä°':'i',
        'Ã‡':'C',
        'Ã–':'O'
        }
        newStr = ''
        for c in repstring:
            if replacedict.get(c) != None:
                newStr = newStr + replacedict[c]
            else:
                newStr = newStr + c
        return newStr
#-    
    def foldercontcre(self,foldername):
        if os.path.exists(foldername) == False:
            os.mkdir(foldername)
            print('Folder creating. ')    
        else:
            print('Folder created. ')       
#-  
    def searchlink(self,source,hrefid,urlsite):
        atagarry = []              
        for atag in tqdm(source.find_all("a"), "Products link are being scanned"):
            atags = urlsite+atag.attrs.get("href")
            atagfind = str(atags).find(hrefid)                            
            if not atags:
                continue
            else:
                if atagfind != -1:
                    if len(atagarry) == 0 or atagarry[len(atagarry)-1] != atags:
                        atagarry.append(atags)
        return atagarry        
#-  
    def downloadimg(self,ahref,findta,folders,urlsite,inputun):
            r = requests.get(ahref)
            source = BeautifulSoup(r.content,"html.parser")           
            for img in tqdm(source.find_all("img"), "Pictures are being scanned"):                   
                img_url = urlsite+"/"+img.attrs.get("src")
                imgnamesp = img.attrs.get("src").split('/')
                img_ex = img.attrs.get("src").split('.')
                img_ex = img_ex[len(img_ex)-1]    
                if not img_url:
                  continue
                else:
                  imgfind = str(img_url).find(findta)
                  if(imgfind != -1 ):
                    if(img_ex == 'jpg' or img_ex == 'png' or img_ex == 'jpeg' or img_ex == 'webp'):                         
                        imgname = folders+"/"+imgnamesp[len(imgnamesp)-1]
                        urllib.request.urlretrieve(img_url,imgname)
                        if inputun.upper() == 'Y':
                            image = Image.open(imgname)
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
                                new_image.save(imgname)
                    else:
                        continue
#-  
    def datamining(self,href,tags,stock,profolder):
        repdict = {
            '<':'',
            '"':'',
            '=':' ',
            '>':''
        }
        retunarray = []
        protags = tags.split(',')
        protags.append(stock)
        r = requests.get(href)
        source = BeautifulSoup(r.content,"html.parser")
        for ptag in protags:
            newStr = ''
            for ptg in ptag:
                if repdict.get(ptg) != None:
                    newStr = newStr + repdict[ptg]
                else:
                    newStr = newStr + ptg
            newStr = newStr.split(' ')
            finds = source.find_all(newStr[0],attrs={newStr[1]:newStr[2]})
            finds = re.sub(r'^.*">', "",str(finds[0])).replace("</"+newStr[0]+">",'')
            retunarray.append(finds)
        return retunarray
#-  
    def creathtmlInfo(self,Infarray,folder):
        html_cd = folder+"/index.html"
        if os.path.exists(html_cd) == False:
            readf = open(html_cd,"a", encoding='utf8')
            html_head = '<html><head><meta charset="utf-8" /><meta http-equiv="x-ua-compatible" content="ie=edge" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>'+Infarray[0]+'</title></head><body>'
            writ = html_head+''.join([str(elem) for elem in Infarray])+'</body></html>'
            datam = readf.write(writ)
            readf.close()
            return print("Index creating.")
        else:                
            return print("Index created.")


                    
             