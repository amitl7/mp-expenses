# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import calendar
import datetime
import pandas as pd
import numpy as np


datasets = os.listdir('datasets/monthly_data')
print (datasets)

alldata = pd.DataFrame()

for monthlydata in datasets: 
    df = pd.read_csv('datasets/monthly_data/{}'.format(monthlydata), skiprows=(5), encoding='cp1252')
    #ignore the first row as its just labels. not needed
    df = df.drop(index =0, axis=0)
    #create date from filename
    filename = monthlydata.split('.')[0]
    monthname = filename.split('-')[0]
    year = filename.split('-')[1]
    
    datetime_object = datetime.datetime.strptime(monthname, "%B")
    month_number = datetime_object.month
    
    date = datetime.date(int(year),int(month_number),int(1))
    monthend = date.replace(day = calendar.monthrange(date.year, date.month)[1])
  
    df['monthend'] = monthend
    
    alldata = alldata.append(df, ignore_index = True)

alldata = alldata.replace('Nil', np.nan)
alldata = alldata.dropna(axis = 1, how = 'all')
alldata.to_csv('datasets/alldata.csv',index = False)
