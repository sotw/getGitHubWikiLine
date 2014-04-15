# Author Pei-Chen Tsai aka Hammer
# Ok, the line break position is impossible to 100% accurate currently, so just tune global parameter for your own purpose

from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib2
import sys


global TYPE_P
global TYPE_H
global TYPE_LI
global BREAK_CNT_P
global BREAK_CNT_H
global BREAK_CNT_LI
TYPE_P = 0
TYPE_H = 1
TYPE_LI = 2
BREAK_CNT_P = 124
BREAK_CNT_H = 96
BREAK_CNT_LI = 120


def contentStrip(iList,iType):
   print 'stripping all tag inside'
   stack = []   
   BREAK_CNT = BREAK_CNT_P #default policy
   
   if iType == TYPE_P :
      BREAK_CNT = BREAK_CNT_P
   if iType == TYPE_H :
      BREAK_CNT = BREAK_CNT_H
   if iType == TYPE_LI :
      BREAK_CNT = BREAK_CNT_LI

   for e in iList:                  
      if e.text is not None :        
        strLength = len(e.text)        
        mod = strLength % BREAK_CNT
        times = strLength / BREAK_CNT
        index = 0
        sliceStart = 0
        sliceEnd = 0
        for index in range(times+1) :         
           if int(index) == int(times):                          
              sliceStart = index*BREAK_CNT
              sliceEnd   = (index)*BREAK_CNT+mod      
              print e.text[sliceStart:sliceEnd]
              stack.append(e.text)
              print len(stack)
           else :
              sliceStart = index*BREAK_CNT
              sliceEnd   = (index+1)*BREAK_CNT            
              print e.text[sliceStart:sliceEnd]
              stack.append(e.text)      
              print len(stack)
   return stack

def handler_p(iList):      
   print '\nENTER p handler'
   ret = len(iList)
   print 'There are %d <p> found' % (ret)
   ret = len(contentStrip(iList,TYPE_P))
   print 'LEAVE p handler'
   return int(ret)

def handler_h(iList):
   print '\nENTER h handler'
   ret = len(iList)
   print 'There are %d <h> found' % (ret)
   ret = len(contentStrip(iList,TYPE_H))
   print 'LEAVE h handler'
   return int(ret)

def handler_li(iList):
   print '\nENTER li handler'
   ret = len(iList)
   print 'There are %d <li> found' % (ret)
   ret = len(contentStrip(iList,TYPE_LI))
   print 'LEAVE li handler'
   return int(ret)

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
   etree.strip_tags(tree,'a')
   etree.strip_tags(tree,'strong')
   etree.strip_tags(tree,'img')
   etree.strip_tags(tree,'span')
   etree,strip_tags(tree,'code')
   
   result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
   #print(result)

   targetURL = ""
   lineSum = 0
   myList = tree.xpath("//div[@class='markdown-body']/p")
   lineSum = handler_p(myList)
   myList = tree.xpath("//div[@class='markdown-body']/h3|\
                        //div[@class='markdown-body']/h2|\
                        //div[@class='markdown-body']/h3|\
                        //div[@class='markdown-body']/h4|\
                        //div[@class='markdown-body']/h5") #[]== this is pretty ugly, any better idea?
   lineSum += handler_h(myList)
   myList = tree.xpath("//div[@class='markdown-body']//li")
   lineSum += handler_li(myList)   
   print "\ntotal lines is %d" %(lineSum)

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
