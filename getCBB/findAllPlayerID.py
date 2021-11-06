import string
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re


url_1 = 'https://www.sports-reference.com/cbb/players/'
url_2 = '-index.html'

alphabet_string = string.ascii_lowercase

alphabet_list = list(alphabet_string)

for letter in alphabet_list:
    fullURL = url_1 + letter + url_2

    req = Request(fullURL)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, "lxml")

    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    for l in links:
        if "players" in l:
            print(l)
