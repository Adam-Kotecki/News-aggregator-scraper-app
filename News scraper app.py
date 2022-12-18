import requests
from bs4 import BeautifulSoup
import os

web = input("Please provide website (Lobsters or Hackers): ")
subject = input("Please provide keyword of subject:")
recent = int(input("How many recent articles to search:"))
provided_points = int(input("Please provide minimal number of points"))

if web == "Hackers":
    website = "https://news.ycombinator.com"
    class1 = '.titleline > a'
    class2 = '.subtext'
if web == "Lobsters":
    website = "https://lobste.rs/"
    class1 = '.u-url'
    class2 = '.score'

res = requests.get(website)
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select(class1)
score = soup.select(class2)

stop = 1

if web == "Hackers":
    if recent > 30:
        if recent == 60:
            stop = 2
        if recent == 90:
            stop = 3
        if recent == 120:
            stop = 4
        if recent == 150:
            stop = 5
if web == "Lobsters":
    if recent > 25:
        if recent == 50:
            stop = 2
        if recent == 75:
            stop = 3
        if recent == 100:
            stop = 4
        if recent == 125:
            stop = 5
        
if web == "Hackers":
    web_page = 'https://news.ycombinator.com/?p='
if web == "Lobsters":
    web_page = 'https://lobste.rs/page/'

    
    for page in range(2, stop + 1):
        res = requests.get(web_page + str(page))
        if res.status_code == 200:
            soup2 = BeautifulSoup(res.text, 'html.parser')
            # Extracting only needed data:
            links2 = soup2.select(class1)
            score2 = soup2.select(class2)
            links = links + links2
            score = score + score2

def interesting_content(links, score):
    content = []
    if web == "Hackers":
        for index, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            points = score[index].select('.score')
            # extracting only articles with points:
            if len(points) > 0:
                points_no = int(points[0].getText().replace(' points', ''))
                # selecting only ones which match criteria:
            if (points_no >= provided_points) and (subject.lower() in title.lower()):
                content.append({'title': title, 'link': href, 'votes': points_no})
    if web == "Lobsters":
        for index, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            points = score[index].getText()
            # extracting only articles with points:
            #if len(points) > 0:
            points_no = int(points)
            if (points_no >= provided_points) and (subject.lower() in title.lower()):
                    content.append({'title': title, 'link': href, 'votes': points_no})
    write_content(content)
    return content

def write_content(content):
    ind = 1
    username = os.environ.get('USER', os.environ.get('USERNAME'))
    with open('C:\\Users\\' + username + '\\Desktop\\Daily content.txt', 'w') as f:
        for dict in content:
            f.write(str(ind) + ". " + str(dict['title']) + " |votes: " + str(dict['votes']) + "|  " + str(dict['link']) + '\n' )
            ind = ind + 1

interesting_content(links, score)