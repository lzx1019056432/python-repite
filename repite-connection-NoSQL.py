import pymongo
import requests
from bs4 import BeautifulSoup

link="https://bbs.hupu.com/lakers-"
number = 1
def mongoconne():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["runoodbd"]
    mycol = mydb["HUPU"]
    return mycol

def insertmongo(mycol,title,author,starttime,replaynumber,browsenumber,endauthors,endreplaytimes):
    mydict = {"title":"title","author":"author","starttime":"starttime","replaynumber":"replaynumber","browsenumber":"browsenumber","endauthors":"endauthors","endreplaytimes":"endreplaytimes"}
    mydict["title"]=title
    mydict["author"]=author
    mydict["starttime"]=starttime
    mydict["replaynumber"]=replaynumber
    mydict["browsenumber"]=browsenumber
    mydict["endauthors"]=endauthors
    mydict["endreplaytimes"]=endreplaytimes
    mycol.insert_one(mydict)

def findallmess(link,number):
    titleset=[]
    authorset=[]
    starttimeset=[]
    replaynumberset=[]
    browsenumberset=[]
    endauthorset=[]
    endreplaytimeset=[]
    link = link+str(number)
    re = requests.get(link)
    soup = BeautifulSoup(re.text,"lxml")
    print(re.text)
    titles = soup.findAll('a',class_='truetit')#.b.text
    authors = soup.findAll('a',class_='aulink')#text
    starttimes = soup.findAll('div',class_='author box')#text.a.find_next_sibling("a")
    replaynumbers = soup.findAll('span',class_='ansour box')#text.split("/")  [0].strip()browsenumber = replaynumber[1].strip()
    endauthors = soup.findAll('span',class_="endauthor")#text
    endreplaytimes = soup.findAll('div',class_="endreply box")#text .a
    for title in titles:
        #print(title.text)
        titleset.append(title.text)
    for author in authors:
        authorset.append(author.text)
    for starttime in starttimes:
        starttimeset.append(starttime.a.find_next_sibling("a").text)
    for replaynumber in replaynumbers:
        replaynumberset.append(replaynumber.text.split("/")[0].strip())
        browsenumberset.append(replaynumber.text.split("/")[1].strip())
    for endauthor in endauthors:
        endauthorset.append(endauthor.text)
    for endreplaytime in endreplaytimes:
        endreplaytimeset.append(endreplaytime.a.text)
    #print(titleset[0]+""+authorset[0]+""+starttimeset[0]+""+replaynumberset[0]+""+browsenumberset[0]+""+endauthorset[0]+""+endreplaytimeset[0])
    mycol = mongoconne()
    for i in range(len(titleset)):
        insertmongo(mycol,titleset[i],authorset[i],starttimeset[i],replaynumberset[i],browsenumberset[i],endauthorset[i],endreplaytimeset[i])

findallmess(link,number)


