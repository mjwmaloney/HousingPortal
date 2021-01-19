import pandas as pd
import glob
from datetime import date

path = 'C:\\Users\\mjwma\\PycharmProjects\\RenoHousing\\CSVs'
#makes a list of all of the CSVs in the folder
all_files = glob.glob(path + '/*.csv')
print(all_files)

#constructs a dataframe that has the info from all of the CSVs
df = pd.concat((pd.read_csv(f, index_col=None, header=0) for f in all_files),ignore_index=True)
if pd.api.types.is_string_dtype(df['Situs']):
    df['Situs'] = df['Situs'].str.strip()

"""
shows the columns in the dataframe
col_list = list(df.columns)
print(col_list)
"""

#filtering to remove owner occupied housing
not_ownocc = df['Situs'] != df['Mailing1']
df_ownocc = df[not_ownocc]

#filtering to get number of properties owned by single owner less than 6
valcounts = df_ownocc.Owner1.value_counts()
smalltime = df.Owner1.isin(valcounts.index[valcounts.lt(6)])
df_oo_smalltime = df_ownocc[smalltime]

#filtering to have owners outside of NV and CA, only SFR, apartments, multifamily
not_instate = (df_oo_smalltime['State'] != 'NV') & (df_oo_smalltime['State'] != 'CA') & ((df_oo_smalltime['BldgType'] == 'Single Family Residence') | (df_oo_smalltime['BldgType'] == 'Townhouse') | (df_oo_smalltime['BldgType'] == 'Apartment') | (df_oo_smalltime['BldgType'] == 'Duplex') | (df_oo_smalltime['BldgType'] == 'MultipleRes (Low Rise)'))
df_oo_st_oos = df_oo_smalltime[not_instate]

#showing sizes of each matrix
print(df.shape)
print(df_ownocc.shape)
print(df_oo_smalltime.shape)
print(df_oo_st_oos.shape)

#convert to excel
df_oo_st_oos.to_excel('RenoData' + date.today().strftime('%b-%d-%Y') + '.xlsx')
print('Successfully written to excel')