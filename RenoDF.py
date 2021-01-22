# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:02:05 2021

bringing FTPaccess, datascrape, and basicDF together to construct a dataframe containing
the tax assessor data, which we save in the HDF5 format for easy access

--------------------------------------------------
Be careful when running this - the datascrape part takes a long time because it redownloads all of the CSVs
--------------------------------------------------

@author: mjwma
"""

import requests
import os
import pandas as pd
import glob
from datetime import date

def FTPaccess():
    """
    this script grabs the first 3 digits of the APN for the tax assessor site
    and writes them into a text file
    """
    
    #creating a text file that has the APN data for Reno's tax assessor site
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
        #print(files)
        folds = [i for i in files if '.pdf' not in i and 'PDF' not in i]
        #print(folds)
        for i in range(len(folds)):
            folds[i] = folds[i][2:]
        #print(folds)
        for i in folds:
            fid.write(i+'\n')
        fid.close()

def datascrape():
    """
    downloads all of the CSVs from the list
    used a get request from the url revealed from f12 --> network --> download csv button
    we knew it was a get request bc clicking on the network activity showed GET in request method section
    """
    
    fid = open('apn2.txt', 'r')
    apn = fid.readlines()
    for i in range(len(apn)):
        apn[i] = apn[i][:-1]
    #print(apn)
    
    print('Downloading CSVs...')
    apn_len = len(apn)
    file_iter = 1
    for i in apn:
        print("Downloading file " + str(file_iter) + " / " + str(apn_len))
        url = 'https://www.washoecounty.us/assessor/cama/qi_list.php?search_term='+i+'&noclosed=0&sonly=strap'
        csv = requests.get(url)
        pathname = os.path.join('C:\\Users\\mjwma\\Desktop\\Python Projects\\HousingPortal\\Reno\\CSVs',i+'.csv')
        with open(pathname,'wb') as output:
            output.write(csv.content)
        file_iter += 1

def basicDF():
    """
    basic dataframe construction, no filtering, etc
    """
    
    path = 'C:\\Users\\mjwma\\Desktop\\Python Projects\\HousingPortal\\Reno\\CSVs'
    #makes a list of all of the CSVs in the folder
    all_files = glob.glob(path + '/*.csv')
    #print(all_files)
    print("All files have been downloaded")
    
    #constructs a dataframe that has the info from all of the CSVs
    df = pd.concat((pd.read_csv(f, index_col=None, header=0) for f in all_files),ignore_index=True)
    print(df.head(10))
    print("Dataframe has been constructed")
    return df

FTPaccess()
datascrape()
df = basicDF()

df.to_hdf('RenoData' + date.today().strftime('%b-%d-%Y') + '.h5', key='df', mode='w')
print("Dataframe has been saved to " + 'RenoData' + date.today().strftime('%b-%d-%Y') + '.h5')