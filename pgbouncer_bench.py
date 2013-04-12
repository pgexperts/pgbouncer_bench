#!/usr/bin/env python

import psycopg2

DBNAME = 'postgres'
DBUSER = 'postgres'

# Set DBHOST = None to use the linux socket
# Note: psycopg2 will honor any libpq environment variables
# in your environment, so make sure you don't have any set 
# if you want to use the unix socket
DBHOST = None
#DBHOST = 'localhost'
DBPORT = 6432

#DBHOST = 'remote-server'
#DBPORT = 5432

def connect():
  connection_string = "dbname=%(dbname)s user=%(dbuser)s" % { 'dbname': DBNAME, 'dbuser': DBUSER }

  if DBHOST is not None:
      connection_string = connection_string + " host=%(dbhost)s" % { 'dbhost': DBHOST }

  if DBPORT is not None:
      connection_string = connection_string + " port=%(dbport)s" % { 'dbport': DBPORT }

  try:
    connection = psycopg2.connect(connection_string)
    connection.autocommit = True
  except:
    print "connection failed!"

  return connection

def bench(query=None):
  db = connect()
  cur = db.cursor()
  cur.execute(query)
  results = cur.fetchall()
  db.commit()
  cur.close()
  db.close()
  del cur
  del db


if __name__ == "__main__":
  for i in range(1, 50000):
    try:
      bench(query="SELECT version()")
    except:
      print "query failed!"
    # print some progress info every 1000 queries
    # so the user doesn't go to sleep
    if i % 1000 == 0:
      print i
