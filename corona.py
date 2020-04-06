#!/usr/bin/env python
# coding: utf-8

# In[39]:


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from flask import Flask, request;
from datetime import datetime;
import re

app = Flask(__name__)

# In[41]:


def numbers():
    req = Request('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=%27')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.findAll('td', attrs={'class': 'number'})
    
    js = ""
    city = ["전국", "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남" ,"제주", "검역"]
    condition = ["증감","확진자","격리해제(완치)","사망", "발생률"]
    i = len(condition);
    c = -1
    js += "{\"state\": \"GOOD\", \"numbers\": ["
    for tag in tags :
        if(i==len(condition)):
            if(c==-1):
                js += "{\"city\": \""+ city[0]+"\""
            else:
                js+= "},{\"city\": \""+ city[c+1]+"\""
            i = 0
            c+=1
        
        js += ",\""+condition[i]+"\": \""+ tag.text +"\""
        
        i+=1
        pass
    js += "}]}"
    last = js.replace("\t", "")
    last = last.replace(" ", "")
    return last.replace("-", "0")
    pass
def world():
    req = Request('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=&brdGubun=&ncvContSeq=&contSeq=&board_id=&gubun=')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.findAll('td', attrs={'class': 'w_bold'})
    
    js = ""
    condition = ["격리중", "격리해제(완치)", "사망", "검사중"]
    country = []
    i = len(condition);
    c = 0
    js += "{\"state\": \"GOOD\" "
    inin = 0
    
    for tag in tags :
        
        if(i==len(condition)):
            if(c==-1):
                js += ""
            else:
                js += "}"
                inin = 1;
            i = 0
            c+=1
        elif(inin == 1):
            country.append(tag.text)
            #js += ",\""+condition[i]+"\": \""+ coco[0] +"\""
        
        i+=1
        pass
    print(country)
    tags = bs.findAll('td', attrs={'class': ''})
    i = 0
    print("ING")
    for tag in tags :
        tt = tag.text.replace(",", "")
        print(tt)
        coco =  re.findall("\d+",tt)
        print(coco)
        js += ",\""+country[i]+"\": \""+ coco[0] +"\""
        
        i+=1
        pass
    return js
    pass
def kor():
    req = Request('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.findAll('td')
    
    js = ""
    condition = ["확진자", "격리해제(완치)","격리중","사망"]
    i = len(condition);
    c = -1
    js += "{\"state\": \"GOOD\" "
    for tag in tags :
        if(i==len(condition)):
            if(c==-1):
                js += ""
            else:
                js += "}"
                break
            i = 0
            c+=1
        
        js += ",\""+condition[i]+"\": \""+ tag.text.replace(" 명", "") +"\""
        
        i+=1
        pass
    return js
    pass

def kakao_kor():
    req = Request('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.findAll('td')
    
    js = ""
    condition = ["확진자", "격리해제(완치)","격리중","사망"]
    i = len(condition);
    c = -1
    js += "{\"version\": \"2.0\", \"template\": {\"outputs\": [ { \"simpleText\": { \"text\": \""
    for tag in tags :
        if(i==len(condition)):
            if(c==-1):
                js += ""
            else:
                js += ""
                break
            i = 0
            c+=1
        
        js += " " + condition[i]+" (은/는) "+ tag.text + "\\n"
        
        i+=1
        pass
    js += " 입니다.\"} }]} }"
    return js
    pass
def kakao_numbers():
    req = Request('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=%27')
    res = urlopen(req)
    html = res.read().decode('utf-8')

    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.findAll('td', attrs={'class': 'number'})
    
    js = ""
    js += "{\"version\": \"2.0\", \"template\": {\"outputs\": [ { \"simpleText\": { \"text\": \""
    city = ["전국", "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남" ,"제주", "검역"]
    condition = ["증감","확진자","격리해제(완치)","사망", "발생률"]
    i = len(condition);
    c = -1
    for tag in tags :
        if(i==len(condition)):
            if(c==-1):
                js += city[0]+" "
            else:
                js += city[c+1]+" "
                
            i = 0
            c+=1
        if(condition[i] == "확진자"):
            js += condition[i]+"는 " + tag.text +"명 \\n"
            pass
        
        
        i+=1
        pass
    js += " 입니다.\"} }]} }"
    last = js.replace("\t", "")
    return last.replace("-", "0")
    pass
@app.route('/corona_numbers')
def index():
    return numbers()
@app.route('/corona_world')
def index_2():
    return world()
@app.route('/corona_korea')
def index_3():
    return kor()
@app.route('/kakao_korea', methods=['POST'])
def index_4():
    return kakao_kor()
@app.route('/kakao_numbers', methods=['POST'])
def index_5():
    return kakao_numbers()
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='90')

# In[ ]:




