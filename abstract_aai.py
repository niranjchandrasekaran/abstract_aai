#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Total number of abstract submissions for each year at AAI')
parser.add_argument('-link', metavar='', help='Table of contents page')

args = parser.parse_args()

if __name__ == '__main__':
    base_link = 'http://jimmunol.org'

    website = args.link
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')

    total = 0

    for topics in soup.find_all('div', {'class': 'issue-toc-section'}):
        for link in topics.find_all('a', href=True):
            new_website = base_link+link['href']
            new_page = requests.get(new_website)
            new_soup = BeautifulSoup(new_page.content, 'html.parser')
            for result in new_soup.find_all('div', {'id': 'search-summary-wrapper'}):
                try:
                    total += int(((result.text.lstrip()).rstrip())[:-8])
                except ValueError:
                    continue

    print('total= %d' % total)
