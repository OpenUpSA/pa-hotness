import requests
import sys
import csv
from bs4 import BeautifulSoup 
from urlparse import urljoin

na_url = "http://www.pa.org.za/organisation/national-assembly/people/?page=8"

def guess_gender(name):
    if name.startswith("Mrs") or name.startswith("Ms"):
        return "F"
    elif name.startswith("Mr"):
        return "M"
    else:
        print name
        print "(M)ale or (F)emale?"
        print ""
        val = raw_input()
        if val.lower() == "m":
            return "M"
        elif val.lower() == "f":
            return "F"
    return "U"

def list_pages():
    list_url = na_url
    while True:
        html = requests.get(list_url).content
        soup = BeautifulSoup(html)
        for item in soup.select(".person-list-item a"):
            url = item["href"]
            if "person" in url:
                yield urljoin(na_url, url)

        next = soup.select("a.next")
        if next:
            list_url = urljoin(na_url, next[0]["href"])
        else:
            break

def detail_page(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html)

    profile_pic = soup.select("div.profile-pic img")
    if profile_pic:
        profile_pic = urljoin(na_url, profile_pic[0]["src"])

    name = soup.select("div.title-space h1")
    if name:
        name = name[0].text

        
    position_title = soup.select("span.position-title")
    if position_title:
        position_title = position_title[0].text
        
    details = soup.select("div.constituency-party a")
    party = details[0].text

    return {
        "url" : url,
        "profile_pic" : profile_pic,
        "name" : name,
        "position_title" : position_title,
        "party" : party,
        "gender" : guess_gender(name),
    }

writer = csv.writer(sys.stdout)
writer.writerow(["url", "pic_url", "name", "position/title", "party"])
def _(s):
    return s.encode("utf8")

for url in list_pages():
    data = detail_page(url)
    writer.writerow([data["url"], _(data["profile_pic"]), _(data["name"]), _(data["position_title"]), _(data["party"])])
    
