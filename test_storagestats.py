# test_pyFSstorageHistory
"""
Unit test fixture for pyFSstorageHistory.py
currently the test assumes that you have built a directory structure
listed below in the setup requirement section.

TODO future versions will build this as part of the unit test setup.
"""

import unittest

from pyFSstorageHistory import *

"""
test setup  depends  on manual creation of the following
directories and files
1 - /testdirs
|___ File_A.txt    1024 b
|___ 2 - /testdirs/subDirBoo
|     |___ File_B.log    50,000,000 b
|     |___ File_C.csv    50,000,000 b
|___ 3 - /testdirs/subDirFoo
      |___ File_D.tar    52,428,800 b
      |___ 4 - /testdirs/subDirFoo/subDirBar
          |___ File_E.py    1024 b

these files are provided for testing in testdirs.zip
"""


#  Basic creation and detection
class TestpyFSstorageHistory(unittest.TestCase):

    def setUp(self):
        self.args = ['-r', 'C:/testdirs', '-l', '1',
                     '-g', 'log_files/run_FSH.log',
                     '-c', 'data_files/FS_History.csv',
                     '-t', 'zip, txt,csv, sql,ps ,log',
                     '-v', '1',
                     '-d', 'true']

        self.root_path = 'C:/testdirs'
        self.monitor_types = ['zip', 'txt', 'csv', 'sql', 'ps', 'log']
        self.log_filename = 'log_files/run_FSH.log'
        self.fs_history_csv_filepath = 'data_files/FS_History.csv'
        self.hist_report_level = 1
        self.myFSstorageHist = pyFSstorageHistory(args=self.args, verbosity=1)

    def tearDown(self):
        pass

    def compareOrderedListOfDicts(self, listA, listB):
        assertEqual = True
        for i in range(len(listA)):
            shared_items = set(listA[i].items()) & set(listB[i].items())
            if 17 != len(shared_items):  # expected number of similar dict entries
                assertEqual = actual & False
        return assertEqual

    def orderedListOfDictsFromCSV(self, file):
        listOfDicts = []
        with open(self.fs_history_csv_filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                listOfDicts.append(row)
        return listOfDicts

    def test_01_parse_cmd_arg(self):
        #setup
        FSstorageHistory = pyFSstorageHistory()
        cmdargs = ['-r', 'C:/testdirs', '-l', '1',
                   '-g', 'log_files/run_FSH.log',
                   '-c', 'data_files/FS_History.csv',
                   '-t', 'zip, txt,csv, sql,ps ,log',
                   '-v', '1',
                   '-d', 'true']
        #test
        actual = FSstorageHistory.parse_cmd_arg(cmdargs, verbosity=1)
        expected = ['C:/testdirs',
                    ['zip', 'txt', 'csv', 'sql', 'ps', 'log'],
                    'log_files/run_FSH.log',
                    'data_files/FS_History.csv', '1',
                    '1',
                    'true']
        self.assertEqual(actual, expected)

    def test_02_dir_totals_by_type(self):
        #test
        actual = self.myFSstorageHist.dir_totals_by_type(self.root_path, self.monitor_types)
        expected = {'ps': 0, 'csv': 0, 'log_Cn': 0, 'log': 0, 'zip': 0, 'ps_Cn': 0, 'zip_Cn': 0, 'other': 0, 'other_Cn': 0, 'sql_Cn': 0, 'sql': 0, 'csv_Cn': 0, 'txt': 1024L, 'txt_Cn': 1}
        self.assertEqual(actual, expected)

    def test_03_dir_tree_info_pars(self):
        #setup
        dirTable = TreeTable()  # init tree
        #test
        self.myFSstorageHist.dir_tree_info_pars(self.root_path, dirTable, self.monitor_types)
        json_str = dirTable.to_json()
        actual = json_str
        expected = '''{"1": {"content": {"ps": 0, "txt": 1024, "log_Cn": 1, "log": 50000000, "zip": 0, "ps_Cn": 0, "txt_Cn": 1, "zip_Cn": 0, "other": 52429824, "sql_Cn": 0, "sql": 0, "other_Cn": 2, "csv": 50000000, "csv_Cn": 1}, "parentid": 1, "children": [2, 3], "nodeid": 1, "name": "C:/testdirs"}, "2": {"content": {"ps": 0, "txt": 0, "log_Cn": 1, "log": 50000000, "zip": 0, "ps_Cn": 0, "txt_Cn": 0, "zip_Cn": 0, "other": 0, "sql_Cn": 0, "sql": 0, "other_Cn": 0, "csv": 50000000, "csv_Cn": 1}, "parentid": 1, "children": [], "nodeid": 2, "name": "C:/testdirs\\\\subDirBoo"}, "3": {"content": {"ps": 0, "txt": 0, "log_Cn": 0, "log": 0, "zip": 0, "ps_Cn": 0, "txt_Cn": 0, "zip_Cn": 0, "other": 52429824, "sql_Cn": 0, "sql": 0, "other_Cn": 2, "csv": 0, "csv_Cn": 0}, "parentid": 1, "children": [4], "nodeid": 3, "name": "C:/testdirs\\\\subDirFoo"}, "4": {"content": {"ps": 0, "txt": 0, "log_Cn": 0, "log": 0, "zip": 0, "ps_Cn": 0, "txt_Cn": 0, "zip_Cn": 0, "other": 1024, "sql_Cn": 0, "sql": 0, "other_Cn": 1, "csv": 0, "csv_Cn": 0}, "parentid": 3, "children": [], "nodeid": 4, "name": "C:/testdirs\\\\subDirFoo\\\\subDirBar"}}'''
        self.assertEqual(actual, expected)

    def test_04_nodeStorageByLeve(self):
        #setup
        dirTable = TreeTable()  # init tree
        self.myFSstorageHist.dir_tree_info_pars(self.root_path, dirTable, self.monitor_types)  # lode dri info into the tree
        #test
        realActual = self.myFSstorageHist.nodeStorageByLeve(dirTable, level=self.hist_report_level)
        realExpected = [{'ps': 0, 'txt': 0, 'log_Cn': 1, 'log': 50000000L, 'zip': 0, 'zz_time': '07:44:17', 'ps_Cn': 0, 'txt_Cn': 0, 'zip_Cn': 0, 'other': 0, 'sql_Cn': 0, 'sql': 0, 'path': 'C:/testdirs\\subDirBoo', 'other_Cn': 0, 'csv': 50000000L, 'zz_level': 2, 'csv_Cn': 1, 'zz_today': '2016-07-12'},
                        {'ps': 0, 'txt': 0, 'log_Cn': 0, 'log': 0, 'zip': 0, 'zz_time': '07:44:17', 'ps_Cn': 0, 'txt_Cn': 0, 'zip_Cn': 0, 'other': 52429824L, 'sql_Cn': 0, 'sql': 0, 'path': 'C:/testdirs\\subDirFoo', 'other_Cn': 2, 'csv': 0, 'zz_level': 2, 'csv_Cn': 0, 'zz_today': '2016-07-12'}
                        ]
        # compare list of dictionaries for equivalents
        actual = self.compareOrderedListOfDicts(realActual, realExpected)
        expected = True
        self.assertEqual(actual, expected)

    def test_05_appendFSHistCSVfile(self):
        #setup
        dirTable = TreeTable()  # init tree
        self.myFSstorageHist.dir_tree_info_pars(self.root_path, dirTable, self.monitor_types)  # lode dir info into the tree
        DirInfoToEmit = self.myFSstorageHist.nodeStorageByLeve(dirTable, level=self.hist_report_level)
        #test
        self.myFSstorageHist.appendFSHistCSVfile(DirInfoToEmit, self.fs_history_csv_filepath, delFile=True)
        # open actual fs_history_csv_filepath for actual to expected comparison
        realExpected = [{'ps': '0', 'txt': '0', 'log_Cn': '1', 'log': '50000000', 'zip': '0', 'zz_time': '09:47:50', 'ps_Cn': '0', 'txt_Cn': '0', 'zip_Cn': '0', 'other': '0', 'sql_Cn': '0', 'sql': '0', 'path': 'C:/testdirs\\subDirBoo', 'csv_Cn': '1', 'csv': '50000000', 'zz_level': '2', 'other_Cn': '0', 'zz_today': '2016-07-12'},
                        {'ps': '0', 'txt': '0', 'log_Cn': '0', 'log': '0', 'zip': '0', 'zz_time': '09:47:50', 'ps_Cn': '0', 'txt_Cn': '0', 'zip_Cn': '0', 'other': '52429824', 'sql_Cn': '0', 'sql': '0', 'path': 'C:/testdirs\\subDirFoo', 'csv_Cn': '0', 'csv': '0', 'zz_level': '2', 'other_Cn': '2', 'zz_today': '2016-07-12'}
                        ]
        # Get Ordered List Of Dicts From the self.fs_history_csv_filepath CSV just loaded
        realActual = self.orderedListOfDictsFromCSV(self.fs_history_csv_filepath)
        # compare list of dictionaries for equivalents
        actual = self.compareOrderedListOfDicts(realActual, realExpected)
        expected = True
        self.assertEqual(actual, expected)

    def test_06_mainBach(self):
        # setup
        fullArgs = ['-r', 'C:/testdirs', '-l', '1',
                    '-g', 'log_files/run_FSH.log',
                    '-c', 'data_files/FS_HistoryFull.csv',
                    '-t', 'zip, txt,csv, sql,ps ,log']
        myNewFSstorageHist = pyFSstorageHistory(args=fullArgs, verbosity=1)
        myNewFSstorageHist.mainBach()
        #test
        # open actual fs_history_csv_filepath for incomparsin
        realExpected = [{'ps': '0', 'txt': '0', 'log_Cn': '1', 'log': '50000000', 'zip': '0', 'zz_time': '09:47:50', 'ps_Cn': '0', 'txt_Cn': '0', 'zip_Cn': '0', 'other': '0', 'sql_Cn': '0', 'sql': '0', 'path': 'C:/testdirs\\subDirBoo', 'csv_Cn': '1', 'csv': '50000000', 'zz_level': '2', 'other_Cn': '0', 'zz_today': '2016-07-12'},
                        {'ps': '0', 'txt': '0', 'log_Cn': '0', 'log': '0', 'zip': '0', 'zz_time': '09:47:50', 'ps_Cn': '0', 'txt_Cn': '0', 'zip_Cn': '0', 'other': '52429824', 'sql_Cn': '0', 'sql': '0', 'path': 'C:/testdirs\\subDirFoo', 'csv_Cn': '0', 'csv': '0', 'zz_level': '2', 'other_Cn': '2', 'zz_today': '2016-07-12'}
                        ]
        # Get Ordered List Of Dicts From the self.fs_history_csv_filepath CSV just loaded
        realActual = self.orderedListOfDictsFromCSV(self.fs_history_csv_filepath)
        # compare list of dictionaries for equivalents
        actual = self.compareOrderedListOfDicts(realActual, realExpected)
        expected = True
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)

## command line test vectors TODO FIND A TEST FRAMWORK
# python pyFSstorageHistory.py -h
# python pyFSstorageHistory.py -l 1 -g "log_files/run_FSH.log" -c data_files/FS_History.csv -t "zip, txt,csv, sql,ps ,log"
# python pyFSstorageHistory.py -r C:/wamp/www -t "php, txt,csv, sql,txt ,log" -l 2
# python pyFSstorageHistory.py -r C:/testdirs -l 1 -g "log_files/run_FSH.log" -c data_files/FS_History.csv -t "zip, txt,csv, sql,ps ,log"
# python pyFSstorageHistory.py -r C:/testdirs -l 1 -g "log_files/run_FSH.log" -v 1
