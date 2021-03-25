__author__ = 'Sidon'

from sqlalchemy import Table, Column, create_engine
from sqlalchemy.orm import sessionmaker
import utils

conf = utils.getconfig('')

def connectToDatabase():
    """Connect to our SQLite database and return a Session object
    This means that the actual filename to be used starts with the characters to the right of the third slash
    An absolute path, which is denoted by starting with a slash, means you need four slashes:
    """
    engine = Connection().connectdb(conf['database'], False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class Singleton:
  def __init__(self, klass):
    self.klass = klass
    self.instance = None
  def __call__(self, *args, **kwds):
    if self.instance == None:
      self.instance = self.klass(*args, **kwds)
    return self.instance


@Singleton
class Connection:

  engine = None

  def connectdb(self, _engine, _echo=False):

    if self.engine is None:
        self.engine = create_engine(_engine, echo=False)
    return self.engine
