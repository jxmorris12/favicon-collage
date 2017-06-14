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
  link_names.append( _t(link_name).lower() )

#
#
# str beautify helper
def _make_dig(s, num_of_dig):
  str_s = str(s)
  while s < 10**(num_of_dig-1):
    s *= 10
    str_s = '0' + str_s
  return str_s
#
#
# special favico redirect links
favico_local = ['fda.gov', 'baidu.com', 'usda.gov', 'businessweek.com', '51.la', 'vice.com', 'ocn.ne.jp', 'epa.gov', 'dribbble.com', 
                'mirror.co.uk', 'dropboxusercontent.com', 'admin.ch', 'nhk.or.jp', 'telnames.net', 'paypal.com', 'umblr.com', 'globo.com',
                'army.mil', 'dot.gov','istockphoto.com', 'ed.gov', 'gpo.gov', 'state.tx.us', 'indiegogo.com']
#
#
# get images
from io import BytesIO
from PIL import Image
import requests
import sys
import time

website_imgs = []
index = 0
num_blank_spaces = 30
print "Downloading images."
num_dig_for_str = str(len(link_names))
_count = 0
_max_count = None
for website_name in link_names:
  if _count == _max_count: break
  _count += 1
  image_url = 'http://' + website_name + '/favicon.ico'
  index += 1
  out_update_str = _make_dig(index, len(num_dig_for_str)) + ' / ' + num_dig_for_str + ' | ' + website_name + ' ' * num_blank_spaces
  sys.stdout.write('%s\r' % out_update_str)
  sys.stdout.flush()
  try:
    # Check for icon in cache
    if website_name in favico_local: 
      raise requests.exceptions.ConnectionError()
    # If not in local storage, get
    response = requests.get(image_url)
    # Sleep for peace of mind
    time.sleep(0)
  except requests.exceptions.ConnectionError:
    try:
      # Site blocks this type of request. Favicon hosted locally
      image_filename = 'ico/' + website_name + '.favicon.ico'
      img = Image.open(image_filename)
      website_imgs.append(img)
      continue
    except Exception as e:
      print "Error at", index, website_name
      print e
      exit(-1)
  try:
    img = Image.open(BytesIO(response.content))
    # For some reason, I have to convert to RGB...
    rgb_img = img.convert('RGB')
    # ...and THEN convert to HSV. It's a quirk of PIL.
    hsv_img = rgb_img.convert('HSV') 
    website_imgs.append(hsv_img)
  except IOError:
    # No image on this page
    website_imgs.append(None)
print
print "Finished image download."

#
#
# hsv color helper methods
# let me discard invalid colors -- too close to black or white (within 2%, I said arbitrarily) 
import numpy
def color_dist(a,b):  
  print a, b
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
  if type(c) == int:
    c = (0, 0, c)
  return not is_too_white(c) and not is_too_black(c) # Haha. De Morgan's law

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
    continue
  img.load()
  pixels = img.getdata()
  w,h = img.size
  hue_tally = 0
  hue_total = 0
  for i in xrange(w):
    for j in xrange(h):
      hsv_val = pixels[(i * h) + j]
      if type(hsv_val) == int: 
        hsv_val = (0, 0, hsv_val) # BW to HSV
      if color_is_valid(hsv_val):
        hue_tally += 1
        hue_total += get_hue_from_color(hsv_val)
  if hue_tally == 0:
    all_image_colors.append(-1)
  else:
    all_image_colors.append(hue_total / float(hue_tally))

print "Finished finding colors."
#
#
# export objects
import json

final_objs = []
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
  final_objs.append( json.dumps(obj) )

#
#
# print
print final_objs
print
print "Exported", len(final_objs), "objects."