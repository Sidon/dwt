__author__ = 'admin'

from sqlalchemy import Table, Column, create_engine


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
        self.engine = create_engine(_engine, echo=_echo)
    return self.engine