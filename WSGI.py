# -*- coding: utf-8 -*-
#打中文
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import plurkapi_g_json as plurkapi_g
import plurkdata,random

class index(webapp.RequestHandler):
        def get(self):
                tv = {'nickname' : self.request.get('u')}
                self.response.out.write(template.render( 'h_index.htm',{'tv' : tv}) )

class end(webapp.RequestHandler):
        def get(self):
                a = random.choice(['h_end.htm' ,'h_end2.htm' , 'h_end3.htm'])
                self.response.out.write(template.render(a,{}))

class qq(webapp.RequestHandler):
       def get(self):
                try:
                        pgg =  plurkapi_g.getplurkpic(self.request.get('u'))
                        import feedparser
                        user_rss = feedparser.parse(('http://www.plurk.com/%s.xml') % pgg.nickname)
                        
                        tv = {
                                'nickname' : pgg.nickname,
                                'uid' : pgg.user_id,
                                'karma' : pgg.karma,
                                'karmach' : pgg.karmach,
                                'friends' : pgg.friends,
                                'fans' : pgg.fans,
                                'location' : pgg.location,
                                'maps' : add_maps(pgg.location,pgg.nickname),
                                'google'  : add_google(pgg.nickname),
                                'powerbar' : morepics(pgg.picsnum),
                                'titlename' : headernote(self.request.get('u')),
                                'getplurkpic' : pgg.getplurkpic(),
                                'user_rss' : user_rss['entries']
                                }
                        #friend_list_top = ("<b>%s</b>'s all pictures %s<br>Karma:%s<br>Location:%s %s<br>") % (pgg.nickname,morepics(pgg.picsnum),pgg.karma,pgg.location,add_maps(pgg.location,pgg.nickname))
                        fds = pgg.getfriend()
                        gf = []
                        for gfn in fds.keys():
                                if fds[gfn]['avatar'] is None:
                                        fds[gfn]['avatar'] = ''
                                gfx = {
                                        'nickname' : fds[gfn]['nick_name'],
                                        'uid' : fds[gfn]['uid'],
                                        'karma' : fds[gfn]['karma'],
                                        'location' : fds[gfn]['location'],
                                        'avatar' : fds[gfn]['avatar'],
                                        #'maps' : add_maps(fds[gfn]['location'],fds[gfn]['nick_name']),
                                        #'google'  : add_google(fds[gfn]['nick_name']),
                                        'powerbar' : morepics(fds[gfn]['avatar'])
                                        }
                                gf.append(gfx)
                        #GET Fans
                        fans = pgg.getfans()
                        gfan = []
                        for gfans in fans.keys():
                                if fans[gfans]['avatar'] is None:
                                        fans[gfans]['avatar'] = ''
                                gfanx = {
                                        'nickname' : fans[gfans]['nick_name'],
                                        'uid' : fans[gfans]['uid'],
                                        'karma' : fans[gfans]['karma'],
                                        'location' : fans[gfans]['location'],
                                        'avatar' : fans[gfans]['avatar'],
                                        #'maps' : add_maps(fds[gfn]['location'],fds[gfn]['nick_name']),
                                        #'google'  : add_google(fds[gfn]['nick_name']),
                                        'powerbar' : morepics(fans[gfans]['avatar'])
                                        }
                                gfan.append(gfanx)
                        self.response.out.write(template.render( 'hh_firstpage.htm' , {'tv' : tv, 'gf' : gf,'gfan' : gfan}) )
                except:
                        self.response.out.write("Please type Plurk ID...")
                
class fls(webapp.RequestHandler):
        def get(self):
                if memcache.flush_all():
                        self.response.out.write("flush_all OK!")
                else:
                        self.response.out.write("ERROR!!")

class girls(webapp.RequestHandler):
        def get(self):
                value = memcache.get("girls")
                seconds = 1800
                if value is None:
                        ddaa = plurkdata.plurkindata2
                        gqls = "where p_gender = 0 and p_upicnum > 50 order by %s %s" % ('p_upicnum',random.choice(['asc','desc']))
                        result = ddaa.gql(gqls)
                        gdata = []
                        for ad in result:
                                gdatax = {
                                                'uname' : ad.p_uname,
                                                'uid' : ad.p_uid,
                                                'upic' : ad.p_upicnum
                                                }
                                gdata.append(gdatax)
                        memcache.add("girls", gdata, seconds)
                else:
                        gdata = value
                bgurl = """正妹 Girls <a href="/boys">猛男 Boys</a> <a href="/star">名人 Star</a> | <a href="/">首頁 Home</a>"""
                tv = {'titlename' : '正妹牆', 'css' : 'girls','bgurl' : bgurl,'seconds' : seconds}
                self.response.out.write(template.render( 'hh_bgpage.htm' , {'gdata' : gdata, 'tv' : tv}) )

class boys(webapp.RequestHandler):
        def get(self):
                value = memcache.get("boys")
                seconds = 1800
                if value is None:
                        ddaa = plurkdata.plurkindata2
                        result = ddaa.gql("where p_gender = 1 and p_upicnum > 50 order by p_upicnum desc")
                        gdata = []
                        for ad in result:
                                gdatax = {
                                                'uname' : ad.p_uname,
                                                'uid' : ad.p_uid,
                                                'upic' : ad.p_upicnum
                                                }
                                gdata.append(gdatax)
                        memcache.add("boys", gdata, seconds)
                else:
                        gdata = value
                bgurl = """<a href="/girls">正妹 Girls</a> 猛男 Boys <a href="/star">名人 Star</a> | <a href="/">首頁 Home</a>"""
                tv = {'titlename' : '猛男牆', 'css' : 'boys','bgurl' : bgurl,'seconds' : seconds}
                self.response.out.write(template.render( 'hh_bgpage.htm' , {'gdata' : gdata, 'tv' : tv}) )

class star(webapp.RequestHandler):
        def get(self):
                value = memcache.get("star")
                seconds = 3600
                if value is None:
                        ddaa = plurkdata.plurkstarindata
                        result = ddaa.gql("order by p_uid")
                        gdata = []
                        for ad in result:
                                if ad.p_upicnum == 0:
                                        p_upicnum = ''
                                else:
                                        p_upicnum = ad.p_upicnum
                                gdatax = {
                                                'uname' : ad.p_uname,
                                                'uid' : ad.p_uid,
                                                'upic' : p_upicnum,
                                                'starinfo' : ad.p_starinfo
                                                }
                                gdata.append(gdatax)
                        memcache.add("star", gdata, seconds)
                else:
                        gdata = value
                bgurl = """<a href="/girls">正妹 Girls</a> <a href="/boys">猛男 Boys</a> 名人牆 Star | <a href="/">首頁 Home</a>"""
                refdata = '<b>Data from <a target="_blank" href="http://briian.com/?p=6170">Briian</a>.</b>'
                tv = {'titlename' : '名人牆', 'css' : 'boys','bgurl' : bgurl,'seconds' : seconds,'refdata' : refdata}
                self.response.out.write(template.render( 'hh_bgpage2.htm' , {'gdata' : gdata, 'tv' : tv}) )

class instar(webapp.RequestHandler):
        def get(self):
                # 1: 歌手、明星、大眾名人
                # 2: 神的領域
                # 3: 部落客、小眾名人
                # 4: 政治人物
                # 5: 電視台、電視節目、傳播媒體、媒體人
                user = users.get_current_user()
                if user:
                        greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
                        inform = """
                                <form action="/instar" method="GET">
                                uname <input name="uname"><br>
                                info <input name="uinfo"><br><input type="submit"></form>
                                """
                        if self.request.get('uname') == '':
                                pass
                        else:
                                pgg =  plurkapi_g.getplurkpic(self.request.get('uname'))
                                try:
                                        picsnum = int(pgg.picsnum)
                                except:
                                        picsnum = 0
                                indata = plurkdata.plurkstarindata(
                                        key_name = pgg.nickname,
                                        p_uname = pgg.nickname,
                                        p_uid = int(pgg.user_id),
                                        p_upicnum = picsnum,
                                        p_gender = int(pgg.gender),
                                        p_startype = 5,
                                        p_starinfo = self.request.get('uinfo')
                                        )
                                #indata.put()
                                self.redirect("/instar")
                        self.response.out.write(inform)
                else:
                        greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/"))

                self.response.out.write("<html><body>%s<br></body></html>" % greeting)

class exif(webapp.RequestHandler):
        def get(self):
                from django.utils import simplejson
                import urllib2
                response = urllib2.urlopen(('http://img2json.appspot.com/go/?url=%s') % self.request.get('p') )
                pic = response.read()
                print "!!!"
                print pic

class rss(webapp.RequestHandler):
        def get(self):
                import feedparser
                d = feedparser.parse('http://www.plurk.com/toomore.xml')
                for a in d['entries']:
                        '''
                        self.response.out.write("#" + a + "<br>")
                        self.response.out.write(d[a])
                        self.response.out.write("<br><br>")
                        '''
                        #wd = a.title + a.updated_parsed
                        self.response.out.write(a.title)
                        self.response.out.write(a.updated_parsed)
                        self.response.out.write("<br>")

def input_uname(arg = None):
        return u"""<form action="/" method="get">
            <div><input name="u" value="%s"> <input type="submit" value="Plurk Picture!">
<div align="right"><a href="http://appengine.google.com/"><img border="0" src="http://code.google.com/appengine/images/appengine-silver-120x30.gif" alt="Powered by Google App Engine" /></a>script type="text/javascript" src="http://widgets.amung.us/classic.js"></script><script type="text/javascript">WAU_classic('9cjt4glh0ecz')</script>
<br><font size="2" color="998899">Plurk Avatar History 1.7-pre<br>噗浪頭像歷史查詢 By <a href="http://www.plurk.com/toomore">Toomore</a></font></div></div>
          </form>
        """ % (arg)

def plurkurlname(name):
        a = {}
        a['goplurk'] = "<a href='./?u=%s'>>>see <b>%s</b> more</a>" % (name,name)
        a['gomore'] = '<a href="./?u=%s"><b>%s</b></a>' % (name,name)
        return a

def morepics(n):
        picurl = '#ffffff'
        m = 'qq'
        try:
                n = int(n)
                if n < 25 :
                        picurl = '#99ff99'
                        m = u'■□□□□'
                elif n < 50 :
                        picurl = '#449944'
                        m = u'■■■□□'
                else:
                        picurl = '#005500s'
                        m = u'■■■■■'
        except:
                n = 0
                picurl = '#ddeedd'
                m = u'□□□□□'
        a = ('<font color="%s">%s</font>') % (picurl,m)
        return a

def add_google(uid):
        plurk = " <a target='_blank' href='http://www.plurk.com/%s'><img border='0' src='http://www.plurk.com/favicon.ico'></a>" % uid
        google = " <a target='_blank' href='http://www.google.com.tw/search?q=%s'><img border='0' src='http://www.google.com.tw/favicon.ico'></a>" % uid
        blogger = " <a target='_blank' href='http://www.google.com/search?q=%s site:blogspot.com'><img width='16' border='0' src='http://www.blogger.com/favicon.ico'></a>" % uid
        wretch = " <a target='_blank' href='http://tw.info.search.yahoo.com/search/wretch?fr=cb-wretch&searchtype=article&p=%s'><img border='0' src='http://www.wretch.cc/favicon.ico'></a>" % uid
        pixnet = " <a target='_blank' href='http://www.pixnet.net/search/%s'><img width='16' border='0' src='http://www.pixnet.net/favicon.ico'></a>" % uid
        twitter = " <a target='_blank' href='http://twitter.com/search?q=%s'><img border='0' src='http://twitter.com/favicon.ico'></a>" % uid
        flickr = " <a target='_blank' href='http://www.flickr.com/search/?q=%s'><img border='0' src='http://www.flickr.com/favicon.ico'></a>" % uid
        picasa = " <a target='_blank' href='http://picasaweb.google.com/lh/view?q=%s&psc=G'><img border='0' src='http://picasaweb.google.com/favicon.ico'></a>" % uid
        yahoo = " <a target='_blank' href='http://tw.search.yahoo.com/search?p=%s'><img border='0' src='http://tw.search.yahoo.com/favicon.ico'></a>" % uid
        a = plurk+twitter+google+yahoo+wretch+blogger+pixnet+flickr+picasa
        return a

def add_maps(n,name):
        if n is None or n == '':
                pass
        else:
                maps = '<a href="http://maps.google.com.tw/maps?q=%s (%s)" target="_blank"><img width="16" border="0" src="http://www.gstatic.com/mgc/images/icons/32x32/maps.png"></a>' % (n,name)
                wikimapia = '<a href="http://wikimapia.org/#search=%s" target="_blank"><img width="16" border="0" src="http://wikimapia.org/favicon.ico"></a>' % n
                return maps+wikimapia

def headernote(name = None):
        if name is None:
                name = ""
        else:
                name = ("[%s] - " % name )
        return name


application = webapp.WSGIApplication([('/user', end),
                                                                ('/',end),
                                                                ('/fls',end),
                                                                ('/girls',end),
                                                                ('/boys',end),
                                                                ('/star',end),
                                                                ('/instar',end),
                                                                ('/exif',end),
                                                                ('/rss',end),
                                                                ('/end',end)
                                                                ],
                                                                debug=True)

def main():
        run_wsgi_app(application)

if __name__ == '__main__':
        main()
