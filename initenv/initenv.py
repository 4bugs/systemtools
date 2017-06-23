#-*- encoding:utf-8 -*-
#!/usr/bin/python

import datetime
import os
import shutil
import sys
import logging
import calendar

# 设置目录

base = '/Users/wangqi/backup/core1'
# now_year = datetime.datetime.now('%Y')
months = 12
# days_this_month = calendar.monthrange()

def initenv():
    # 创建base目录
    os.system('mkdir -p %s' % base)
    # 创建月份目录
    for m in range(months):
        os.system('mkdir -p %s' % os.path.join(base,str(m)))

if __name__ == '__main__':
    initenv()