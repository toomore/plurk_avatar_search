# import urllib,urllib2,re,random,cookielib
import urllib,urllib2,re,random,plurkdata
from django.utils import simplejson
from google.appengine.api import memcache
#import simplejson
# nickname = 'inaiko'

class getplurkpic:
        def __init__(self,arg,size = 'big'):
                self.nickname = str(arg)
                self.user_id =  -1
                self.karma = "-1"
                self.karmach = 0
                self.location = "TW"
                self.picsnum = '0'
                self.gender = 0
                self.friends = 0
                self.fans = 0
                self.page = "qw"
                self.size = size
                self.finduid()
        
        def finduid(self):
                """finduid"""
                response = urllib2.urlopen('http://www.plurk.com/%s' % (self.nickname) )
                self.page = response.read()
                uid_pat = re.compile('var GLOBAL = (\{.*\})')
                matches = uid_pat.findall(self.page)
                matches[0] = matches[0].replace("new Date","")
                matches[0] = matches[0].replace('("','"')
                matches[0] = matches[0].replace('")','"')
                test_json = simplejson.JSONDecoder().decode(matches[0])
                # http://avatars.plurk.com/703365-big4.jpg
                #u_pic = re.compile('http://avatars\.plurk\.com/.*-big([\d]+)\.jpg')
                self.nickname = test_json['page_user']['nick_name']
                self.picsnum = test_json['page_user']['avatar']
                self.gender = test_json['page_user']['gender']
                self.user_id = test_json['page_user']['uid']
                self.karma = test_json['page_user']['karma']
                self.karmach = test_json['page_user']['karma_change']
                self.location = test_json['page_user']['location']
                self.friends = test_json['page_user']['num_of_friends']
                self.fans = test_json['page_user']['num_of_fans']
                #TEST Vars ======                
                #print self.user_id
                #print u_pic_m
                #print "qq" + self.user_id + "qq"
                #print self.karma
                #print u_pic_m[0]
                #print "!!!"
                #print test_json
                #print "ASDF:",dir(u_pic_m)

        def getplurkpic(self):
                #IN DATA
                try:
                        int(self.picsnum)
                except:
                        self.picsnum = 0
                if self.picsnum is None or self.picsnum == 'None' :
                        return self.printpic(0 , self.size)
                else:
                        indata = plurkdata.plurkindata2(key_name = self.nickname,
                                p_uname = self.nickname,
                                p_uid = int(self.user_id),
                                p_upicnum = int(self.picsnum),
                                p_gender = int(self.gender)
                                )
                        indata.put()
                        return self.printpic(self.picsnum , self.size)
        
        def getfriend(self):
                #response = urllib2.urlopen('http://www.plurk.com/%s' % (self.nickname) )
                #page = response.read()
                #uid_pat = re.compile('var FRIENDS = \{.*"nick_name": "([\w]+)*",.*\}')
                #uid_pat = re.compile('"nick_name": "([\w]+)*"')
                #matches = uid_pat.findall(self.page)
                uid_pat = re.compile('var FRIENDS = (\{.*\})')
                matches = uid_pat.findall(self.page)
                matches[0] = matches[0].replace("new Date","")
                matches[0] = matches[0].replace('("','"')
                matches[0] = matches[0].replace('")','"')
                test_json = simplejson.JSONDecoder().decode(matches[0])
                return test_json

        def getfans(self):
                uid_pat = re.compile('var FANS = (\{.*\})')
                matches = uid_pat.findall(self.page)
                matches[0] = matches[0].replace("new Date","")
                matches[0] = matches[0].replace('("','"')
                matches[0] = matches[0].replace('")','"')
                test_json = simplejson.JSONDecoder().decode(matches[0])
                return test_json
        
        def printpic(self,x,size):
                try:                
                        x = int(x)
                except:
                        x = 0
                y = []
                y.append(x)
                while x > 0:
                        x = x -2
                        if x > 1:
                                y.append(x)
                else:
                        y.append('')
                #for i in y:
                        #picurl = "http://avatars.plurk.com/%s-%s%s.jpg" % (self.user_id,size,i)
                        #op_pic = op_pic + ('<a href="/exif?p=%s"><img border="0" alt="" src="%s"></a>\n' % (picurl,picurl) )
                #op_pic = op_pic + ('<img alt="" src="http://avatars.plurk.com/%s-%s.jpg">\n' % (self.user_id,size))
                #return op_pic
                return y
