import requests
from bs4 import BeautifulSoup
import os

subject = input("Please provide keyword of subject:")
recent = int(input("How many recent articles to search:"))
provided_points = int(input("Please provide minimal number of points"))

res = requests.get('https://lobste.rs/')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.u-url')
scores = soup.select('.score')

stop = 1

if recent > 25:
    if recent == 50:
        stop = 2
    if recent == 75:
        stop = 3
    if recent == 100:
        stop = 4
    if recent == 125:
        stop = 5
    
    for page in range(2, stop + 1):
        res = requests.get('https://lobste.rs/page/' + str(page))
        if res.status_code == 200:
            soup2 = BeautifulSoup(res.text, 'html.parser')
            # Extracting only needed data:
            links2 = soup2.select('.u-url')
            scores2 = soup2.select('.score')
            links = links + links2
            scores = scores + scores2

def interesting_content(links, scores):
    content = []
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        points = scores[index].getText()
        points_no = int(points)
        # selecting only ones which match criteria:
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

interesting_content(links, scores)
