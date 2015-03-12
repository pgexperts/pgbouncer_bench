pgbouncer_bench
===============

hacked together script to benchmark pgbouncer vs destroying and recreating a
connection for every single query

usage: ./pgbouncer_bench.py

edit the variables at the top to specify which host and ports to run against.

Should've added command line arguments, but needed this in a hurry.

If you use this with greater than about 28,000 connections being created and destroyed on linux, you probably need to modify the following sysctl variable or you'll run out of sockets because they'll be in TIME_WAIT.

```
net.ipv4.tcp_tw_reuse = 1
```
There's a great writeup about that here: 
http://vincent.bernat.im/en/blog/2014-tcp-time-wait-state-linux.html
