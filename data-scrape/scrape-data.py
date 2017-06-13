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

soup = BeautifulSoup(open("./moz-top-sites.html"), 'lxml')

top_500_table = soup.find(id='top-500')
top_site_urls = top_500_table.find_all("td",attrs={"class":"url"})

#
#
# get links
link_names = []
for url in top_site_urls:
  link_name = url.find('a').text
  link_names.append( _t(link_name) )

#
#
# get images
from io import BytesIO
from PIL import Image
import requests

website_imgs = []
x = 0
for website_name in link_names:
  image_url = 'http://' + website_name + '/favicon.ico'
  response = requests.get(image_url)
  try:
    img = Image.open(BytesIO(response.content)).convert('HSV')
    website_imgs.append(img)
  except IOError:
    website_imgs.append(None)
  x += 1
  if x > 3: break

#
#
# hsv color helper methods
# let me discard invalid colors -- too close to black or white (within 2%, I said)
import numpy
def color_dist(a,b):  
  # math.hypot should support three arguments :( 
  x = a[0] - b[0]
  y = a[1] - b[1]
  z = a[2] - b[2]
  return (x**2 + y**2 + z**2) ** .5

_black = (0, 0, 0)
_white = (0, 0, 255)
_threshold = color_dist(_black, (255,255,255)) * .02
def is_too_black(c):
  return color_dist(_black, c) < _threshold

def is_too_white(c):
  return color_dist(_white, c) < _threshold

def color_is_valid(c):
  return not (is_too_white(c) or is_too_black(c))

def get_hue_from_color(hsv):
  return hsv[0]

#
#
# average image hue
all_image_colors = []
for img in website_imgs:
  if not img:
    # No favicon.ico found
    all_image_colors.append(-1)
    break
  img.load()
  pixels = img.getdata()
  w,h = img.size
  hue_tally = 0
  hue_total = 0
  for i in xrange(w):
    for j in xrange(h):
      hsv_val = pixels[(i * h) + j]
      if color_is_valid(hsv_val):
        hue_tally += 1
        hue_total += get_hue_from_color(hsv_val)
  all_image_colors.append(hue_total / float(hue_tally))

#
#
# export objects
import json
for x in xrange(len(all_image_colors)):
  site_url = link_names[x]
  dot_pos = site_url.index('.')
  site_name = site_url[:dot_pos]
  site_tld = site_url[dot_pos+1:]
  site_favicon_hue = all_image_colors[x]
  obj = {
    'name': site_name,
    'tld': site_tld,
    'hue': site_favicon_hue
  }
  print json.dumps(obj) + ','