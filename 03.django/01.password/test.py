#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.contrib.auth.hashers import make_password, check_password
print( "你好" )

# 原密码 1234
password = '1234'
# 加密
make_password(password) # pbkdf2_sha256$120000$S92tuv6RM7Ct$SwDIx5MYxahhSCFWf/OmA650rZTvqbW7QcbNLw/Oq/I=

# 加密后的密码
pwd = 'pbkdf2_sha256$120000$S92tuv6RM7Ct$SwDIx5MYxahhSCFWf/OmA650rZTvqbW7QcbNLw/Oq/I='

# 校验密码  如果相同则返回True 否则返回False
check_password('1234',pwd)
