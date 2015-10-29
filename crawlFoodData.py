#!/usr/bin/env  python
# This Python file uses the following encoding: utf-8

import urllib2,httplib
import threading,Queue,re
import sys,socket,time,random
from HTMLParser import HTMLParser
from functools import wraps
from gzip import GzipFile
from StringIO import StringIO

class ContentEncodingProcessor(urllib2.BaseHandler):
  """A handler to add gzip capabilities to urllib2 requests """
  
  # add headers to requests
  def http_request(self, req):
    req.add_header("Accept-Encoding", "gzip, deflate")
    return req
  
  # decode
  def http_response(self, req, resp):
    old_resp = resp
    # gzip
    if resp.headers.get("content-encoding") == "gzip":
      gz = GzipFile(
        fileobj=StringIO(resp.read()),
        mode="r"
        )
      resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
      resp.msg = old_resp.msg
    # deflate
    if resp.headers.get("content-encoding") == "deflate":
      gz = StringIO( deflate(resp.read()) )
      resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
      resp.msg = old_resp.msg
    return resp
  
# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
  try:               # so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)

# create a subclass and override the handler methods                                                    
class FoodHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.count = 0
    self.data = ''
    self.result = '{'
    self.isNext = False;
    
    def handle_starttag(self, tag, attrs):
      self.data +=  '\'' + tag + '\':'

    def handle_data(self, data):
      print data
      if data.strip() != '':
        self.data += '\''+ data.strip() + '\','
            #print self.data
        self.result += self.data
        self.data = ''
        if self.isNext:
          self.result = self.result[:-1] + '}'
          print self.result 
          self.isNext = False;
          self.result = '{'
          self.count += 1

def get_food_url(self):
  cname = "pinyin.txt"
  with open(cname) as f:
    city_list = f.readlines()
    
  pname = 'proxy.txt'
  with open(pname) as f:
    proxy_list = f.readlines()

  uname = 'useragent.txt'
  with open(uname) as f:
    userAgent_list = f.readlines()
    
  for city in city_list:
    proxy = random.choice(proxy_list)
    userAgent = random.choice(userAgent_list)
    time.sleep(1)
    print "###### " + city.strip()  
    url = 'http://api.nuomi.com/api/dailydeal?version=v1&city=' + city.strip()
    processData(url, proxy, userAgent)

def retry(ExceptionToCheck, tries=3, delay=3, backoff=2, logger=None):
  def deco_retry(f):

    @wraps(f)
    def f_retry(*args, **kwargs):
      mtries, mdelay = tries, delay
      while mtries > 1:
        try:
          return f(*args, **kwargs)
        except ExceptionToCheck, e:
          msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
          if logger:
            logger.warning(msg)
          else:
            print msg
            time.sleep(mdelay)
            mtries -= 1
            mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


def processData(url,proxy, userAgent):
  try:
    encoding_support = ContentEncodingProcessor
    proxy_handler = urllib2.ProxyHandler({"http" : r'' + proxy.strip() })
    opener = urllib2.build_opener(encoding_support)#, proxy_handler)
    opener.addheaders = [('User-agent', userAgent[:-2]),('Accept-Encoding',"gzip, deflate")]
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url.strip(), timeout=5000)
    result = req.read()
    parser = FoodHTMLParser()
    parser.feed(result)
    parser.close()
  except urllib2.URLError, e:
    print "Time out error."
    reProcessData(url, proxy, userAgent)
  except socket.error, e:
    print "Connection Refused:" + proxy
    reProcessData(url, proxy, userAgent)
  except httplib.BadStatusLine:
    print "Bad status line:" + proxy
    reProcessData(url, proxy, userAgent)
  except httplib.IncompleteRead as e:
    print "IncompleteRead over long."
    reProcessData(url, proxy, userAgent)


def reProcessData(url,proxy, userAgent):
  try:
    encoding_support = ContentEncodingProcessor
    proxy_handler = urllib2.ProxyHandler({"http" : r'' + proxy.strip() })
    opener = urllib2.build_opener(encoding_support)#, proxy_handler)
    opener.addheaders = [('User-agent', userAgent[:-2]),('Accept-Encoding',"gzip, deflate")]
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url.strip(), timeout=5000)
    result = req.read()
    parser = FoodHTMLParser()
    parser.feed(result)
    parser.close()
  except urllib2.URLError, e:
    print "Time out error."
    pass
  except socket.error, e:
    print "Connection Refused:" + proxy
    pass
  except httplib.BadStatusLine:
    print "Bad status line:" + proxy
    pass
  except httplib.IncompleteRead as e:
    print "IncompleteRead over long."
    pass
  
if __name__ == '__main__':
  print "######## Start  crawling Nuomi data ########"
  get_food_url(None)
  print "######## Finish crawling Nuomi data ########"
  






