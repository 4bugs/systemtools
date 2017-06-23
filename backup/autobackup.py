import os, shutil
import datetime
import logging


def log_thread():
    logPath = '/tmp/mv.log'
    if os.path.exists(logPath)==False:
        os.system('touch /tmp/mv.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s %'
                               '(levelname)s %(message)s',
                        datefmt='%a,%b %Y %H:%M:%S',
                        filename='%s' % logPath,
                        filemode='a'
                        )

def get_host_id(eth_path):
    try:
        networkfile = open(eth_path, 'r')
        networkfile_lines = networkfile.readlines()
        for line in networkfile_lines:
            if line[0:6]=='IPADDR':
                host_id = line[-2:]
    finally:
        networkfile.close()
    return  host_id


def mv_files():
    log_thread()
    logging.info("====================%s====================" % (datetime.datetime.now().strftime('%Y%m%d')))
    host_id = get_host_id('/Users/wangqi/tmp/ifcfg-eth2')
    # backup 60 days ago files
    backupDate = datetime.datetime.now() - datetime.timedelta(days=60)
    # archive 90 days ago files
    archiveDate = datetime.datetime.now() - datetime.timedelta(days=90)
    mvYearMonth = backupDate.strftime('%Y%m')
    mvDay = backupDate.strftime('%d')
    arcYearMonth = archiveDate.strftime('%Y%m')
    arcDay = archiveDate.strftime('%d')
    src_dir = ('/Users/wangqi/databak/%s/%s') % (mvYearMonth, mvDay)
    dst_dir = (("/Users/wangqi/backup/core%s/%s") % (host_id, mvYearMonth)).replace("\n", "")
    arc_dir = (('/Users/wangqi/backup/core%s/%s/%s') % (host_id, arcYearMonth, arcDay)).replace("\n", "")
    if os.path.exists(dst_dir)==False:
        os.system('mkdir -p %s' % dst_dir)

    if os.path.exists(src_dir) and os.path.exists((dst_dir + '/%s') % mvDay)==False:
        # moving files
        shutil.move(src_dir, dst_dir)
        logging.info('%s has been moving to  %s' % (src_dir, dst_dir))
    elif os.path.exists(src_dir) and os.path.exists((dst_dir + '/%s') % mvDay) :
        os.system('cd %s && ls |xargs -I {} mv {} %s/{}' % (src_dir, dst_dir))
        logging.info("%s is already moved to " % src_dir)
    else:
        logging.info("%s has been moving to, Nothing to do. " % src_dir)

    # archive
    print arc_dir
    if os.path.exists(arc_dir) and os.path.exists(arc_dir + 'tar.gz')==False:
        shutil.make_archive(arc_dir, 'gztar', arc_dir)
        logging.info('%s has been archived now.' % arc_dir)
    elif os.path.exists(arc_dir + '.tar.gz'):
        logging.info('%s already exsits.' % (arc_dir + 'tar.gz'))


if __name__ == '__main__':
    mv_files()