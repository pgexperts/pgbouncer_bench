#!/usr/bin/env python
#
#    pgbouncer_bench.py is licensed under the PostgreSQL License:
#
#    Copyright (c) 2012, PostgreSQL, Experts, Inc.
#
#    Permission to use, copy, modify, and distribute this software and its
#    documentation for any purpose, without fee, and without a written
#    agreement is hereby granted, provided that the above copyright notice and
#    this paragraph and the following two paragraphs appear in all copies.
#
#    IN NO EVENT SHALL POSTGRESQL EXPERTS, INC. BE LIABLE TO ANY PARTY FOR
#    DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
#    LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
#    DOCUMENTATION, EVEN IF POSTGRESQL EXPERTS, INC. HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGE.
#
#    POSTGRESQL EXPERTS, INC. SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
#    BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS"
#    BASIS, AND POSTGRESQL EXPERTS, INC. HAS NO OBLIGATIONS TO PROVIDE
#    MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
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
