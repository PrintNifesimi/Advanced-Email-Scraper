import requests
from bs4 import BeautifulSoup
import time,re
import csv

global filename
filename=""

fields=['name','email']
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
    global filename
    filename=",".join(searchTerms.split())
    url =f'https://www.google.com/search?q={mutate(website,"website")}+{mutate(searchTerms,"searchTerms")}+"icloud"+OR+"outlook"+OR+"gmail"+OR+"yahoo"'
    print(url)
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
def getHtml(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    return soup

def scrapeDataInstagram(html):
    #first get the users username from url instagram.com/userName/
    
    #URLS=html.findAll("div",{"class":"egMi0 kCrYT"})#.a.get("href")
    #emailContainer=html.findAll("div",{"class":"BNeawe s3v9rd AP7Wnd"})
    infoDiv = html.findAll("div",{"class":"Gx5Zad fP1Qef xpd EtOod pkphOe"})
    uNRegex=getRegex("instagramUN")
    emailRegex=getRegex("emailRegex")
    
    rows=[]
    for info in infoDiv:
        url=info.a
        if url:
            url = url.get("href")
        else:
            url = None
        userName=uNRegex.search(url).group() if url else None
        if userName == "p":userName="From Post"
        emails=emailRegex.findall(info.find("div",{"class":"BNeawe s3v9rd AP7Wnd"}).text)
        if emails==[]:continue
        emailToWrite=""
        for emailGroup in emails:
            emailToWrite+=" "+emailGroup[0] #getting all emails in div incase more than one
        lst=[userName]+emailToWrite.split()
        rows.append(lst) #append this pages usernames and emails to rows for csv file

#Write to csv file 
    with open(f"({filename})info.csv",mode='a') as infoFile:
            csvFile = csv.writer(infoFile)
            #join all emails if multiple
            global fields
            if fields:
                csvFile.writerow(fields)
                
                fields=[]
            
            csvFile.writerows(rows)
    infoDiv=[]
    
    return 

def nextPage():
    url = buildURL() #User builds URL on first attempt
    
    while url:
        time.sleep(3)
        html=getHtml(url)
        scrapeDataInstagram(html)
        prevAndNext=html.findAll("a",{"class":"nBDE1b G5eFlf"})
        if len(prevAndNext)==0:return "Done Scraping"
        url = "https://www.google.com"+prevAndNext[-1].get("href")
    
    

    


print(nextPage())