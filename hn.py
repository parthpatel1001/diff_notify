import re
from urlparse import urlparse
from lxml import html
from lxml.cssselect import CSSSelector as css
import requests
''' look for amazon links in hn comments'''

base_url = 'https://news.ycombinator.com/news'
comment_url = 'https://news.ycombinator.com/item'
num_pages = 10

def hn_params(page_num):
  return { 'p': page_num }

def hn_page_html(base_url, params):
  return requests.get(base_url, params=params).content

def get_els(page_html, selector='.athing'):
  for tr in css(selector)(html.fromstring(page_html)):
    a = css('a')(tr.getchildren()[2])[0]
    yield tr, a

def comments_params(tr):
  return {'id' : tr.get('id')}

def comments_html(comment_url, params):
  return requests.get(comment_url, params=params).content

def comment_els(comment_html, text_class='.c00', match_on='.*amazon\.co.*\/.*|.*amzn\.co.*\/.*'):
  for comment in css(text_class)(html.fromstring(comment_html)):
    links = css('a')(comment)
    for link in links:
      if 'reply' not in link.text and re.match(match_on, link.get('href')) and 'aws.' not in link.get('href'):
        yield comment, link
    #if comment.text and re.match(match_on, comment.text):
      #yield comment

for page_num in range(1, num_pages + 1):
  for (tr, a) in get_els(hn_page_html(base_url, hn_params(page_num))):
    c_els = comment_els(
      comments_html(comment_url, comments_params(tr))
    )
    print 'Searching', a.text, '...'
    for (comment, link) in c_els:
      print '\t','---'*5
      print '\t',comment.text_contents()
      print '\t', link.get('href')
      print '\t','---'*5
      

