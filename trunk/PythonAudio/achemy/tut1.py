import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import Column, Integer, String


class User(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    
    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
   
   
   
   
print User.__table__ 
print User.__mapper__



Base.metadata.create_all(engine)

ed_user = User('ed', 'Ed Jones', 'edspassword')

print ed_user



from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session  = Session()

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()


session.add_all([User('wendy', 'Wendy Williams', 'foobar'),\
   User('mary', 'Mary Contrary', 'xxg527'),\
   User('fred', 'Fred Flinstone', 'blah')])

print our_user

ed_user.password = 'f8s7ccs'

#session.dirty

our_user = session.query(User).filter_by(name='ed').first()


print our_user

session.commit()