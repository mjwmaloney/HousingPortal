"""this script grabs the first 3 digits of the APN for the tax assessor site
and writes them into a text file, which we will then iterate over using selenium
to download the data in csv format for analysis"""

#creating a text file that has the APN data for Reno's tax assessor site
import re
from ftplib import FTP

#opening the FTP session - must use the URL without any subdirectories
with FTP('wcftp.washoecounty.us') as ftp:
    print(ftp.getwelcome())
    ftp.login()
    ftp.cwd('outtoworld/assessor-books')
    print('We are currently in')
    print(ftp.pwd())
    #gets a list of all of the file/directory names
    files = ftp.nlst()
    fid = open('apn2.txt','w')
    iteration = 0
    print(files)
    folds = [i for i in files if '.pdf' not in i and 'PDF' not in i]
    print(folds)
    for i in range(len(folds)):
        folds[i] = folds[i][2:]
    print(folds)
    for i in folds:
        fid.write(i+'\n')
    fid.close()