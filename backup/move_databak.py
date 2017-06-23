#!/usr/bin/python

import datetime
import os
import shutil
import sys
import logging


# set the id of the server
HOST_ID = 1

# set the query dir
QUERY_DIR = '/databack'

# set the percent of the QUERY_DIR deadline
PER = 79

# set the log path
LOG_PATH = '/tmp/archive.log'

# set the base backup dir
BACKUP_BASE = '/backup/uss-core%s/' % HOST_ID

# set the des dir
DEST_BASE = '/backup/core%s' % HOST_ID


# logging the thread
def log_thread():
    if not os.path.exists(LOG_PATH):
        os.system('touch %s' % LOG_PATH)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s %'
                               '(levelname)s %(message)s',
                        datefmt='%a,%b %Y %H:%M:%S',
                        filename='%s' % LOG_PATH,
                        filemode='a'
                        )


# get the /backup useage percent
def disk_backup():
    disk = os.statvfs(QUERY_DIR)
    percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail)
    return percent

def the_move():
    # find the src dir
    src_dir = ''
    dst_dir = ''
    shutil.move(src_dir, dst_dir)

def move():
    now_per = disk_backup()
    logging.info('Now %s is %s%%' % (QUERY_DIR ,now_per))
    while now_per > PER:
        the_move()
        now_per = disk_backup()
    else:
        logging.info('the space is enough!')
        sys.exit(0)
