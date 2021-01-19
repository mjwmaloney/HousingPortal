# this code works --> downloads all of the CSVs from the list
# used a get request from the url revealed from f12 --> network --> download csv button
# we knew it was a get request bc clicking on the network activity showed GET in request method section
import requests
import os

fid = open('apn2.txt', 'r')
apn = fid.readlines()
for i in range(len(apn)):
    apn[i] = apn[i][:-1]
print(apn)

#we just have the index part in because it stopped after that one for some reason on first run
for i in apn[apn.index('132'):]:
    url = 'https://www.washoecounty.us/assessor/cama/qi_list.php?search_term='+i+'&noclosed=0&sonly=strap'
    csv = requests.get(url)
    pathname = os.path.join('C:\\Users\\mjwma\\PycharmProjects\\RenoHousing\\CSVs',i+'.csv')
    with open(pathname,'wb') as output:
        output.write(csv.content)