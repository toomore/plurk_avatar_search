from google.appengine.ext import db
class plurkindata2(db.Model):
        p_uname = db.StringProperty()
        p_uid = db.IntegerProperty()
        p_upicnum = db.IntegerProperty()
        p_date = db.DateTimeProperty(auto_now_add = True)
        p_chdate = db.DateTimeProperty(auto_now = True)
        p_gender = db.IntegerProperty()

class plurkstarindata(db.Model):
        p_uname = db.StringProperty()
        p_uid = db.IntegerProperty()
        p_upicnum = db.IntegerProperty()
        p_date = db.DateTimeProperty(auto_now_add = True)
        p_chdate = db.DateTimeProperty(auto_now = True)
        p_gender = db.IntegerProperty()
        p_startype = db.IntegerProperty()
        p_starinfo = db.StringProperty()
