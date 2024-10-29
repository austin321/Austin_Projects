import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

visited_urls = set()

def spider_urls(url, keyword): #pass specific URLs and keywords that we want to see
    try:
        response = requests.get(url) 

    except:
        print(f"Request failed {url}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')
        urls = []

        #for every href that isn't an empty string, it will append
        #the value to our empty list
        for tag in a_tags:
            href = tag.get('href')
            if href is not None and href != "":
                urls.append(href)


    #    print(urls)
    for urls2 in urls:
        if urls2 not in visited_urls:
            visited_urls.add(url) #going to visited urls and seeing if it has been visited
            url_join = urljoin(url, urls2) 
            if keyword in url_join:
                print(url_join)
                spider_urls(url_join, keyword)
        else:
            pass


# https://blog.badsectorlabs.com/




url = input("enter the url that we wanna scrape: ")
keyword = input("enter the keyword to search for in the URL provided: ")
spider_urls(url, keyword)