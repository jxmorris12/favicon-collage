# jack morris 06/12/17
# data are from https://moz.com/top500, scraped today
#
#
# unicode helper
def _u(s):
  return s.encode('utf-8')
#
#
# string helper
def _t(s):
  return _u(s).strip()
#
#
# BeautifulSoup scrape
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("./moz-top-sites.html"))

top_500_table = soup.find(id='top-500')
top_site_urls = top_500_table.find_all("td",attrs={"class":"url"})

link_names = []
for url in top_site_urls:
  link_name = url.find('a').text
  link_names.append( _t(link_name) )

print link_names