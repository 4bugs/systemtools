#!/usr/bin/python

import datetime
import os
import shutil
import sys
import logging

# set the id of the server
HOST_ID = 2 

# set the query dir
QUERY_DIR = '/backup'

# set the percent of the QUERY_DIR deadline
PER = 79

# set the log path
LOG_PATH = '/tmp/archive.log'

# set the base backup dir
BACKUP_BASE = '/backup/core%s/' % HOST_ID



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

def archve_trc():
    """
        find the dir need to be archive
    """
    # find the server's need to be archived month dir
    MONTH_DIR = []
    DAY_DIR = []
    months_dirs = os.listdir(BACKUP_BASE)
    for month_dir in months_dirs:
        if 'tar.gz' not in month_dir and 'bak' not in month_dir:
            MONTH_DIR.append(month_dir)
    # get the full path of the archive month dir
    try:
        arc_mon_dir = BACKUP_BASE + min(MONTH_DIR)
        arc_mon_dir_list = os.listdir(BACKUP_BASE + min(MONTH_DIR))
    except ValueError:
        logging.info("no files need to be archived")
        logging.info('================Ending================')
        sys.exit(0)

    # find the days dir need to be archived
    for day_dir in arc_mon_dir_list:
        if 'tar.gz' not in day_dir:
            DAY_DIR.append(day_dir)
    # find the day dir need to be archived
    try:
        arc_day_dir = BACKUP_BASE + min(MONTH_DIR) + '/' + min(DAY_DIR)
    except ValueError:
        arc_day_dir = ''
    # archive the day need to be archived and remove the day dir
    if os.path.exists(arc_day_dir):
        print arc_day_dir
        logging.info('---archiving the %s ...---' % arc_day_dir)
        os.system('cd %s && tar -czf %s.tar.gz %s' %
                  (arc_mon_dir, min(DAY_DIR), min(DAY_DIR)))
        logging.info('%s has been archived.' % arc_day_dir)
        logging.info('%s will be removed' % arc_day_dir)
        shutil.rmtree(arc_day_dir)
        logging.info('%s has been removed' % arc_day_dir)
        DAY_DIR.pop(DAY_DIR.index(min(DAY_DIR)))
    else:
        logging.info('---archiving the %s---' % arc_mon_dir)
        # shutil.make_archive(arc_mon_dir, 'gztar', arc_mon_dir)
        os.system('cd %s && tar -czf %s.tar.gz %s' %
                  (BACKUP_BASE, min(MONTH_DIR), min(MONTH_DIR)))
        logging.info('%s has been archied' % arc_mon_dir)
        logging.info('%s will be removed' % arc_mon_dir)
        shutil.rmtree(arc_mon_dir)
        logging.info('%s has been removed' % arc_mon_dir)
        logging.info('================Ending================')
        sys.exit(0)

def need_to_be_archived():
    now_per = disk_backup()
    logging.info('Now %s is %s%%' % (QUERY_DIR ,now_per))
    while now_per > PER:
        archve_trc()
        now_per = disk_backup()
    else:
        logging.info('the space is enough!')
        sys.exit(0)

if __name__ == '__main__':
    log_thread()
    logging.info("================Starting================")
    need_to_be_archived()
