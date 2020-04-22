#############################################################
#   File Name: py_call_c.py
#     Autohor: Hui Chen (c) 2020
#        Mail: chenhui13@baidu.com
# Create Time: 2020/04/22-11:04:42
#############################################################
#!/usr/bin/env python 
#-*- coding:utf8 -*-

import ctypes

libadd = ctypes.cdll.LoadLibrary( ".//libadd.so" )
print "1 add 2 is", libadd.add( 1, 2 )
