import urlparse
from lxml import html
from lxml.cssselect import CSSSelector as css
import requests
''' get contract jobs in ny, skipping filtered jobs'''

base_url = 'http://newyork.craigslist.org/search/sof/'
num_pages = 15
res_per_page = 100
employment_type = 3 # contract
filters = [
  'java ', # space is intentional, <3 javascript
  'ldap', 
  'ios', 
  'android',
  'data entry', 
  'C#', 
  '.NET',
  'BA/QA', 
  'Business Analyst'
]

def cl_params(page_num, res_per_page, employment_type):
  return {
    's': page_num * res_per_page,
    'employment_type' : employment_type
  }

def cl_page_html(base_url, params):
  return requests.get(base_url, params=params).content

def get_els(page_html, filters, selector='.hdrlnk'):
  ''' yields (to_crawl, skip) '''
  for el in css(selector)(html.fromstring(page_html)):
    if any((i.upper() in el.text.upper() for i in filters)):
      yield el, None
    else:
      yield None, el

for page_num in range(0, num_pages):
  els = get_els(
    cl_page_html(
      base_url, 
      cl_params(page_num, res_per_page, employment_type)
    ),
    filters
  )
  for (skip, crawl) in els:
    if skip is None:
      print crawl.text, '\t', urlparse.urljoin(base_url, crawl.get('href'))
