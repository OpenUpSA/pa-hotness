from sqlalchemy import Column, Integer, String
from .views import db


class MemberOfParliament(db.Model):

    def __init__(self, url=None, profile_pic=None, name=None, detail=None, party=None, gender=None):
        self.url = url
        self.profile_pic = profile_pic
        self.name = name
        self.detail = detail
        self.party = party
        self.gender = gender
        if url:
            self.key = url.split('/')[-2]
        return

    __tablename__ = 'members'

    # columns
    pk = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    url = Column(String)
    party = Column(String)
    profile_pic = Column(String)
    key = Column(String)
    score = Column(Integer, default=0)

    def __repr__(self):
        return "<MemberOfParliament(pk='%s', name='%s')>" % (
            str(self.pk), str(self.name))

    def as_dict(self):
       tmp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
       del tmp['pk']
       del tmp['key']
       tmp['id'] = self.key
       return tmp
