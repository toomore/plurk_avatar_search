from google.appengine.ext import db
class plurkindata2(db.Model):
        p_uname = db.StringProperty()
        p_uid = db.IntegerProperty()
        p_upicnum = db.IntegerProperty()
        p_date = db.DateTimeProperty(auto_now_add = True)
        p_chdate = db.DateTimeProperty(auto_now = True)
