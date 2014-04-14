# Author Pei-Chen Tsai aka Hammer
# Ok, this is simple script to parse line in github

from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib2
import sys


def htmlParser(tPage):
   resp = urllib2.urlopen(tPage)
   if resp.code == 200 :
      data = resp.read()
      resp.close()
   else :
      print('can not open page')
      exit()
   parser = etree.HTMLParser()
   tree = etree.parse(StringIO(data), parser)
   result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
   #print(result)

   targetURL = ""
   mylist = tree.xpath(".//div[@class='markdown-body']/p")
   print 'Analying...there are %d link found' % (len(mylist))   


def main():
   tPage = 'https://github.com/'+sys.argv[1]+'/wiki'
   print('target is:'+tPage)
   htmlParser(tPage)

def verify():
   if len(sys.argv)!=2:
      print "you need to input x/y where is inside 'https://github.com/x/y/wiki'"
      exit()

if __name__ == '__main__':
   verify()
   main()
