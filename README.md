[![Build Status](https://travis-ci.org/jayventi/storagestats.svg?branch=master)](https://travis-ci.org/jayventi/storagestats)
##storagestats##

### Description ###
storagestats is intended as a command line utility which analyzes local disk storage utilization starting at a specific root directory and summing files stored under that directory by types which are specifiable. Each node contains utilization statistics for that node and all of its child nodes down to the leaf directories. That is, space utilization is summed for a list of subcategories such as *.log files. Not only do specific types in a directory contribute to the sums for the directory but also all of their child directories recursively. The output is appended to a CSV file with one row per directory containing utilization statistics plus pathname, tree level, and date-time the utility ran. The intent is to produce an output file that can be used to produce time series statistics by a secondary program. Only a subset of the directories are output to the CSV file this is determined by a level parameter which restricts the number of output directories to those contained within a specified number of levels below the root directory.

###Background###
This utility is designed to produce statistics to allow the monitoring of data file growth where data is deposited as sets of flat files written to a file system using a directory structure as a cataloging system. It is imagined that this utility will be run as a line command in a cron process periodically monitoring storage growth of a given directory structure. It is assumed that some other program will be responsible for digesting the historical information produced by this utility. storagestats is specifically designed to monitor directory structures which grow but do not shrink, there are no provisions made for handling or annotating changes that occur in a directory structure.

## Installation ##
Deploy all the files and directories from the git repository to a convenient directory, install python dependencies described below. storagestats.py should now be executable.

### Output files and directories###
When executed output CSV files will be written to data_files/FSHistory.csv and log files to log_files/run_log.log. These values are configurable on the command line if you use different paths they will need to be created before used.


##Python dependencies##

**scandir**
https://github.com/benhoyt/scandir

scandir Is included in Python 3.3 and higher
As os.scandir, see github scandir readme.


##storagestats Command line##



    storagestats.py -r <root_path> -t <monitor_types> -g <log_filename> -c <fs_history_csv_filepath> -l <hist_report_level> -d <del_csv> -v <verbosity>

 `<root_path>` = Base directory storagestats will collect statistics on this directory and all child directories, this is the root reference point from which storage is calculated. When specifying a Windows directory it's recommended to use  '/' as the directory separator in the pathname, otherwise use "\\" on window pathnames.
 
 `<monitor_types>` = A list given in the form [ 'file_prefix',... ] which, defines the file types that sums are separately calculated for, example ['zip', 'txt', 'csv', 'sql', 'log']. In the output CSV file, there will be one column for each specifier listed, storage values of zero will be given if no such files appear in the directory or its children. Additionally, for each specifier a secondary column will be included which gives the file count for the number of files contributing to the totals, they take the form of file_prefix+'_Cn'. Additionally, in all cases, a category 'other' is automatically inserted and contains the sums of all files not falling into the types listed in the monitor_types list

 `<log_filename>` =  Base log file name, defaults to `log_files/run_log.log` if not specified. Files are round robin deleted according to parameters set in loger_tool.py.

 `<fs_history_csv_filepath\>` = Filename of the csv output file, if not specified defaults to 'data_files/FSHistory.csv'.

 `<hist_report_level\>` = Specifies the number of levels in the tree which are to be reported on and emitted to the history_csv_filepath file. Level 1 indicates the immediate children directories reciting in the root directory will be transcribed and added to the csv file and no others.

 `<del_csv>` = Controls whether the csv history file's is deleted or not. If it is set to true, 1, true or True any existing csv file matching the name given by fs_history_csv_filepath will be deleted if it exists, a new file will then be written. The default is to append and not to delete.

 `<verbosity>` = Controls' the verbosity of console print status statements, there are three supported levels 1,2 and 3;  1, quiet state, no status information printed, 2,  most status statements are printed, and 3  all statement printed.  Does not affect log status entries which are unaffected by verbosity.

## Unittest ##
Two unit tests files are provided, one for the underlying tree storage object test_treeTable.py, and one for the main program test_storagestats.py. The latter requires a specific directory structure to test against. The test directory structure may be installed from testdirs.zip deployed to your test directory this directory needs to be referenced in test_storagestats.py.

## Known limitations ##

#### 256 path length error on Windows filesystems ####
On a Windows file system, scandir returns an error on names longer than 256 characters, this error is logged as a warning and execution continues but pathnames longer than 256 will not be included in the sums. There is a known win workaround see: use win32api (pywin32) to 'build' up a shorter path version.
