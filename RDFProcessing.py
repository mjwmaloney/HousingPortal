# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:37:37 2021

A file containing functions used to sort and filter the Reno dataframe. Requires RenoDF to be run prior to usage

@author: mjwma
"""

from datetime import date
import pandas as pd

#the master copy of the data
_df = pd.read_hdf('RenoData' + date.today().strftime('%b-%d-%Y') + '.h5')

#the mutable copy of the data
df = _df



def filter_not_ownocc(frame):
    """
    Returns a dataframe of properties where the mailing address differs from the property address
    """
    
    if pd.api.types.is_string_dtype(df['Situs']):
        frame['Situs'] = frame['Situs'].str.strip()
    not_ownocc = frame['Situs'] != frame['Mailing1']
    df_not_ownocc = frame[not_ownocc]
    return df_not_ownocc

def filter_propnum(frame, propnum):
    """
    Returns a dataframe of properties where the owner does not own more than propnum properties
    """
    
    valcounts = frame.Owner1.value_counts()
    smalltime = frame.Owner1.isin(valcounts.index[valcounts.lt(propnum)])
    df_smalltime = frame[smalltime]
    return df_smalltime

def filter_state(frame, states):
    """
    Returns a dataframe of properties excluding the states in the states list
    """
    
    state_frame = frame
    for i in states:
        excl_state = frame['State'] != i
        state_frame = state_frame[excl_state]
    return state_frame

def filter_bldg_type(frame, bldg_type=
                     ['Townhouse','Single Family Residence','Multiple Res (Low Rise)','High-Value Residence','Duplex','Apartment']):
    """
    Returns a dataframe of properties including only the building types in the bldg_type list
    """
    
    bldg_type_frame = frame
    for i in bldg_type:
        incl_type = frame['BldgType'] == i
        bldg_type_frame =frame[incl_type]
    return bldg_type_frame

def gt_beds(frame,beds):
    """
    Returns a dataframe of properties with number of bedrooms greater than than the number entered
    """
    
    bed_logic = frame['Beds'] > beds
    gt_beds_frame = frame[bed_logic]
    return gt_beds_frame

def ge_beds(frame,beds):
    """
    Returns a dataframe of properties with number of bedrooms greater than than the number entered
    """
    
    bed_logic = frame['Beds'] >= beds
    ge_beds_frame = frame[bed_logic]
    return ge_beds_frame

def lt_beds(frame,beds):
    """
    Returns a dataframe of properties with number of bedrooms greater than than the number entered
    """
    
    bed_logic = frame['Beds'] < beds
    lt_beds_frame = frame[bed_logic]
    return lt_beds_frame

def le_beds(frame,beds):
    """
    Returns a dataframe of properties with number of bedrooms greater than than the number entered
    """
    
    bed_logic = frame['Beds'] <= beds
    le_beds_frame = frame[bed_logic]
    return le_beds_frame

def eq_beds(frame,beds):
    """
    Returns a dataframe of properties with number of bedrooms greater than than the number entered
    """
    
    bed_logic = frame['Beds'] == beds
    eq_beds_frame = frame[bed_logic]
    return eq_beds_frame

if __name__ == "__main__":
    #print(df)
    #print(filter_not_ownocc(df))
    print(df.shape)
    print(filter_state(df,['CA']).shape)
    print(filter_state(df,['NV']).shape)
    print(filter_state(df,['CA','NV']).shape)