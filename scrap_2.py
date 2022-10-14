# Scrap Hacker News project and save the result in a csv file.
#  The csv file should have the following columns: title, link,
#   points, comments, author, rank. The csv file should be sorted 
#   by rank in ascending order.

from bs4 import BeautifulSoup
import csv 
import requests



url ="https://news.ycombinator.com/"
r = requests.get(url)

# print(r.status_code)

html_page = BeautifulSoup(r.content,'html.parser')
# print(html_page.prettify())

news_page = html_page.find('table',class_ = "itemlist")
articles = news_page.find_all('tr',class_ = "athing")

for article in articles:
    if article == None:
        continue
    title = article.find('span',class_ = 'titleline').a.text
    link =article.find('span',class_ = 'titleline').a['href']
    points = article.find('span',class_ = "score").text
    print(points)
    exit()

# print(news_page)d

