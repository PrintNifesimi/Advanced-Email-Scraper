import requests
from bs4 import BeautifulSoup
import time,re


#mutation of strings for appropriate search ()
def mutate(userInput:str,infoToChange:str)->str:
    if infoToChange == 'website':
        return "site%3A"+userInput.strip()
    if infoToChange == 'searchTerms':
        lst=userInput.split()
        for i in range(len(lst)):
            lst[i]=f'"{lst[i]}"'
        return "+OR+".join(lst)
    

#Get Search Information from User
def buildURL():
    website=input("Enter A Site To Search e.g (instagram.com): ").strip()
    searchTerms = input("Enter 1-3 optional search Terms: ")
    url =f'https://www.google.com/search?q={mutate(website,"website")}+{mutate(searchTerms,"searchTerms")}+"icloud"+OR+"outlook"+OR+"gmail"+OR+"yahoo"'
    return url

#Regex for email,usernames,etc
def getRegex(inquiry):
    instagramUN=re.compile(r'(?<=instagram.com\/)[A-Za-z0-9_.]+')
    emailRegex=re.compile(r'''(
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    (\.[a-zA-Z]{2,4})
    )''',re.VERBOSE)
    regexDict = {"instagramUN":instagramUN,"emailRegex":emailRegex}
    return regexDict[inquiry]

#Handle Html
def getHtml(bool,url=None):
    html = requests.get(buildURL()) if bool else requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    return soup

def scrapeDataInstagram():
    #first get the users username from url instagram.com/userName/
    html=getHtml(True)
    #URLS=html.findAll("div",{"class":"egMi0 kCrYT"})#.a.get("href")
    #emailContainer=html.findAll("div",{"class":"BNeawe s3v9rd AP7Wnd"})
    infoDiv = html.findAll("div",{"class":"Gx5Zad fP1Qef xpd EtOod pkphOe"})
    uNRegex=getRegex("instagramUN")
    emailRegex=getRegex("emailRegex")
    for info in infoDiv:
        url=info.a
        if url:
            url = url.get("href")
        else:
            url = None
        userName=uNRegex.search(url).group() if url else None
        emails=emailRegex.findall(info.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text)
        if emails==[]:continue
        print(userName,"  ",emails,"\n")
        with open("info.txt",mode='a') as infoFile:
            #join all emails if multiple
            emailToWrite=""
            for emailGroup in emails:
                emailToWrite+=","+emailGroup[0]
            infoFile.write(userName+emailToWrite+"\n")

    return ""




print(getHtml(True))