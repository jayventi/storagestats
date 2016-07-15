
""" 
FileSystem Storage History utility
StorageStats: FileSystem Storage Statistics utility is a command line
utility which is file system agnostic. It collecting file size statistics
for each directory within a given root directory. statistics are written
to a node tree which emulates the branching structure of the file system
branch given by the root directory. A given node contains summarized
statistics for itself and all children and subchildren. Utilizes scandir
for file system accesswhich must be added for python 2.7

python 2.7
Created on Jun 23, 2016
@author: jayventi
"""

# python 2.7 import
import os.path
import csv
import sys
import getopt

from time import gmtime, strftime, time

# scandir a 2.7 dependency
from scandir import scandir

# this project
from loger_tool import *
from utilitys.treetable import TreeTable


class StorageStats(object):
    """
    Main package orchestrates execution for StorageStats utility
    StorageStats.main orchestrates main execution
    """
    def str2bool(slef, v):
        return v.lower() in ("yes", "true", "t", "1") if v else None

    def __init__(self,
                 root_path= 'C:\work\Dojo',
                 monitor_types=['js', 'zip', 'txt', 'csv', 'sql', 'ps', 'log'],
                 log_filename='log_files/run_log.log',
                 fs_history_csv_filepath='data_files/FSHistory.csv',
                 hist_report_level=2,
                 del_csv='false',
                 args='',
                 verbosity=2
                 ):  # set defalt config values
        self.verbosity = verbosity
        cmd_arg = self.parse_cmd_arg(args, self.verbosity)
        self.root_path = cmd_arg[0] or root_path
        self.monitor_types = cmd_arg[1] or monitor_types
        self.log_filename = cmd_arg[2] or log_filename
        self.fs_history_csv_filepath = cmd_arg[3] or fs_history_csv_filepath
        self.hist_report_level = int(cmd_arg[4] or hist_report_level)
        self.verbosity = int(cmd_arg[5] or verbosity)
        self.del_csv = self.str2bool(cmd_arg[6]) or self.str2bool(del_csv)
        self.today = strftime("%Y-%m-%d", gmtime())
        self.crtime = strftime("%H:%M:%S", gmtime())

        # set up log handler
        self.log_handler = loger_mang(log_path=self.log_filename)
        # log info written
        logging.info('Starting pyStoigyNodeHistory.py main scrip exicqtion')
        logging.info('ROOT_PATH: {}'.format(self.root_path))
        logging.info('MONITOR_TYPES: {}'.format(self.monitor_types))
        logging.info('LOG_FILENAME: {}'.format(log_filename))
        logging.info('FS_HISTORY_CSV_FILEPATH: {}'.format(self.fs_history_csv_filepath))
        logging.info('HIST_REPORT_LEVEL: {}'.format(self.hist_report_level))

    def dir_totals_by_type(self, path, monitor_types):
        """
        Returns a dictionary with a keys set to each monitor types
        The value is the long total size in bytes.
        Fof each monitor file type an additional key is produced 
        "types +'_Cn'" for file count value set to integer file 
        count for that type. all files not falling under 
        monitor_types are summarized in the default category 
        'other'
        """
        dir_info = {}
        other, other_Cn = 0, 0
        for k in monitor_types:
            dir_info[k], dir_info[k+'_Cn'] = 0, 0
        try:
            dirEntryList = scandir(path)
            for entry in dirEntryList:
                if not entry.is_dir(follow_symlinks=False):
                    thisType = entry.name.split('.')[-1]
                    if thisType in monitor_types:
                        dir_info[thisType] += entry.stat(follow_symlinks=False).st_size
                        dir_info[thisType + '_Cn'] += 1
                    else:
                        other += entry.stat(follow_symlinks=False).st_size
                        other_Cn += 1
        except Exception as e:
            logging.warn( e )
        dir_info['other'], dir_info['other_Cn'] = other, other_Cn
        return dir_info


    def dir_tree_info_pars(self, path, dirtrtable, monitor_types):
        """
        Recursively traverses the filesystem, loads the dirtrtable tree object
        Return a dir_info dict with statistics from it's children
        adds a dirtrtable dir node if none exises and sets the node content 
        to dir_info. Traverses filesystem using breath first method.
        Main algorithmic worker for StorageStats.
        """
        if not dirtrtable.isNodeByName(path):  # if this dir has no dir node in dirtrtable make one
            if not dirtrtable.isRootSet():  # dirtrtable has only a uninitialized root node, root needs initialization
                dirtrtable.setRootName(path, {})  # init the root node set to this the first root dir path
            else:
                parNodeId = dirtrtable.getNodeIdByName(os.path.dirname(path))
                dirtrtable.addChild(path, parNodeId, {})
        dir_info = self.dir_totals_by_type(path, monitor_types)

        try:
            for entry in scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    temp_dir_info = self.dir_tree_info_pars(os.path.join(path, entry.name), dirtrtable, monitor_types)
                    for each in dir_info:
                        dir_info[each] += temp_dir_info[each]
        except Exception as e:
            logging.warn( e )
        dirtrtable.upDateNodeByName(path, dir_info)
        return dir_info


    def nodeStorageByLeve(self, dir_info_tree, level=0, nodeId=1):
        """
        Emits a list of dir info dicts for level depth in dir_info_tree,
        starting with nodeId, uses breath first tree traversal.
        """
        level += 1
        dirInfoRows = []
        childNodeList = dir_info_tree.getChildren(nodeId)
        if len(childNodeList) > 0:  # if not a leaf node precess childNodes
            dirInfoRows = [{}] * len(childNodeList)
            for i in range(len(childNodeList)):
                dirnode = dir_info_tree.getNodeById(childNodeList[i])
                dirInfoRows[i] = self.buildDirInfo(dirnode, level)
            if level < self.hist_report_level:
                # Now iterate over children
                for childNodeId in childNodeList:
                    ChildrenRows = self.nodeStorageByLeve(dir_info_tree, level, childNodeId)
                    if len(ChildrenRows) > 0:  # id rows produced build/ extend new dirInfoRows list
                        dirInfoRows = dirInfoRows + ChildrenRows
        return dirInfoRows


    def buildDirInfo(self, dirnode, level):
        """
        Build directory information dictionary
        by augmenting dirnode.content additional information
        """
        fomatedDirInfo = dirnode.content
        fomatedDirInfo['zz_today'] = self.today
        fomatedDirInfo['zz_time'] = self.crtime
        fomatedDirInfo['zz_level'] = level
        fomatedDirInfo['path'] = dirnode.name
        return fomatedDirInfo


    def appendFSHistCSVfile(self,  storageDateList, csv_filename, delFile=False):
        """
        Appends DirInfo data as a single row to a CSV file
        Given a list of DirInfo dictionaries as storageDateList, append each
        as a row to csv_filename.
        If delFile=True instead of appending tcsv_filename will be deleted 
        if it exists.
        """
        pathFieldName = 'path'
        file_exists = os.path.isfile(csv_filename)
        if delFile & file_exists:
            try:
                os.remove(csv_filename)
                file_exists = False
            except Exception as e:
                logging.warn( e )
                return
        fieldnames = storageDateList[0].keys()
        headers = fieldnames
        headers.remove(pathFieldName)
        headers.sort()
        headers.append(pathFieldName)
        strx = 'appendFSHistCSVfile: serializing: {0} dir node entries to: {1}'\
            .format(len(storageDateList), csv_filename)
        logging.info(strx)
        if self.verbosity >= 2:
            print strx
        t1 = time()
        try:
            with open(csv_filename, 'a') as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    lineterminator='\n',
                    extrasaction='ignore',
                    fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()  # file doesn't exist yet, write a header
                writer.writerows(storageDateList)
                t2 = time()
                strx = 'appendFSHistCSVfile: took: {0:.2f} seconds'.format(t2 - t1)
                logging.info(strx)
                if self.verbosity >= 2:
                    print strx
        except Exception as e:
            logging.warn( e )


    def parse_cmd_arg(self, cmdargs, verbosity=2):
        """
        Parses, incoming command line arguments
        uses getopt to parse commandline if format described
        is matched than parameters are set, other wise
        error conditions echoed to terminal
        """
        root_path, monitor_types, log_filename, fs_history_csv_filepath, \
            hist_report_level, verbos, del_csv = [None] * 7
        try:
                opts, args = getopt.getopt(cmdargs, "r:t:g:c:l:v:d:h",
                                           ["--root", "--MonType",
                                            "--LogFiles", "--HisCSV",
                                            "--Leve", "--Verbos",
                                            "--DelCSV", "--help"
                                            ])
        except getopt.GetoptError:
                print('try -h')
                sys.exit(2)
        for opt, arg in opts:
            if verbosity >= 3:
                print("opt : ", opt)
                print("arg : ", arg)
            if opt in ("-h", "--help"):
                    prtstr = '''
                     StorageStats.py -r <root_path> -t <monitor_types> -g <log_filename>
                     -c <fs_history_csv_filepath> -l <hist_report_level> -d <del_csv> -v <verbosity>
                     '''
                    print(prtstr)
                    sys.exit()
            elif opt in ("-r", "--root"):
                    root_path = arg
            elif opt in ("-t", "--MonType"):
                    monitor_types = "".join(arg.split()).split(',')
            elif opt in ("-g", "--LogFiles"):
                    log_filename = arg
            elif opt in ("-c", "--HisCSV"):
                    fs_history_csv_filepath = arg
            elif opt in ("-l", "--Leve"):
                    hist_report_level = arg
            elif opt in ("-v", "--Verbos"):
                    verbos = arg
            elif opt in ("-d", "--DelCSV"):
                    del_csv = arg
        # print 'return',[root_path, monitor_types, log_filename, fs_history_csv_filepath, hist_report_level, verbos]
        return [root_path, monitor_types, log_filename, fs_history_csv_filepath, hist_report_level, verbos, del_csv]

    def mainBach(self):
        """
        Orchestrates main execution for StorageStats
        """
        if not os.path.isdir(self.root_path):
            prtstr = 'Root file path {} does not exist StorageStats aborted'. \
                format(self.root_path)
            logging.info(prtstr)
            print('{} \n'.format(prtstr))
            return

        new_dir_info_tree = TreeTable()  # init tree

        #get new dir info run  dir_tree_info_pars
        prtstr0 = 'Running dir_tree_info_pars'
        logging.info(prtstr0)
        self.dir_tree_info_pars(self.root_path, new_dir_info_tree, self.monitor_types)
        prtstr1 = 'Total number of directory scanned: {}'
        logging.info(prtstr1.format(new_dir_info_tree.nodeCount()))

        # setup date for output, emit a dict of info fore each dir in tree
        # down to tree depth of self.hist_report_level
        DirInfoToEmit = self.nodeStorageByLeve(new_dir_info_tree)
        if self.verbosity >= 2:
            print('\n{}\n'.format(prtstr0))
            print(prtstr1.format(new_dir_info_tree.nodeCount()))
        # write or append csv of FSstorageHistoryCSV
        # TODO exspose to comand line delFile=False
        self.appendFSHistCSVfile(DirInfoToEmit, self.fs_history_csv_filepath, self.del_csv)

        prtstr2 = 'Done pyStoigyNodeHistory main scrip execution ends'
        logging.info(prtstr2)
        loger_mang(stop_handler=self.log_handler)  # shutdown log handler

        if self.verbosity >= 2:
            print('')
            print('{} \n'.format(prtstr2))
            # for fun
            new_dir_info_tree.prettyTreeTable()

        return True


## **************  main  *************** ##

def main(args):

    # initialize
    mystoragestats = StorageStats(args=args)

    # run, scandir, build tree, output csv
    mystoragestats.mainBach()

if __name__ == '__main__':
        main(sys.argv[1:])
