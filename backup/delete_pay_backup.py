#-*- encoding:utf-8 -*-
#!/usr/bin/python

import os
import shutil
import sys
import logging

# set the query dir
QUERY_DIR = 'databak/'

# set the percent of the QUERY_DIR deadline
PER = 79

# set the log path
LOG_PATH = '/tmp/archive.log'


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

def delete_databak():
    # find the dir to delete
    month_dir = QUERY_DIR + min(os.listdir(QUERY_DIR))
    try:
        dst_dir = month_dir + '/' + min(os.listdir(month_dir))
        logging.info('Removing %s ...' % dst_dir)
        shutil.rmtree(dst_dir)
        logging.info('%s has been removed.' % dst_dir)
    #if can't find the day dir ,then pop ValueError,then delete the month dir
    except ValueError:
        logging.warning('Nothing in %s' % month_dir)
        logging.info('Removing %s...' % month_dir)
        shutil.rmtree(month_dir)
        logging.info('%s has been removed.' % month_dir)

def need_to_be_archived():
    now_per = disk_backup()
    logging.info('Now %s is %s%%' % (QUERY_DIR ,now_per))
    while now_per > PER:
        delete_databak()
        now_per = disk_backup()
    else:
        logging.info('the space is enough!')
        sys.exit(0)

if __name__ == '__main__':
    log_thread()
    logging.info("================Starting================")
    delete_databak()