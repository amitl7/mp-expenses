#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:34:41 2021

@author: amitlandge
"""
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import os
import numpy as np

    
def get_expenses(filename, classname):
    claims= {
        'id':[],
        'date':[],
        'type':[],
        'description':[],
        'amount':[]
        }
    
    souplist = []
    
    with open(f'datasets/mp_exp_html/{filename}', 'r') as html_file:
        
        name = filename.replace('.html','')
        
        content = html_file.read()
        
        soup = BeautifulSoup(content, 'lxml')
        
        
        lookupclass = soup.find_all('div', class_ =f'{classname}')
            
        print (name, 'starting')
        
    for exp in lookupclass:

        souplist.append(exp.get_text().replace('\n',' ').split('    ')   )

    souplist = [[val.strip() for val in lst if val] for lst in souplist]
    
    claims = {'id':[],'date':[],'type':[],'description':[],'amount':[]}
    
    for key in claims:
        for lst in souplist:
            try:
                claims[key].append(lst[lst.index(key.title())+1])
            except ValueError:
                if key == 'id':
                    claims[key].append(lst[2])
                else:
                    claims[key].append(None)
                   
    df = pd.DataFrame(claims)
    df.date = pd.to_datetime(df.date)
    
    try:
        
        df['sub_type'] = [str(x).split(' (')[-1].replace(')','') for x in df['type']]
        
        df['type'] = [str(x).split(' (')[-0] for x in df['type']]
        
        df['amount'].fillna(0, inplace = True)
        df['status'] = [str(x).split(' ')[-1].replace('0','Unknown') for x in df['amount']]
        df['amount'] = [str(x).split(' ')[-0] for x in df['amount']]
        
        df['name'] = name
        
        df.amount = df.amount.str.replace('£','')
    
    except:
        pass
 
    print(name, 'complete')
    
    return df
  
  
def create_csv(scrape1,scrape2):
    
    path = 'datasets/mp_exp_html'

    files = os.listdir(path)

    
    for f in files:
        
        mp_name = f.replace('.html','')
                            
        df = get_expenses(f,scrape1 )
        df1 = get_expenses(f,scrape2 )
        
        frames = [df,df1]
        alldata = pd.concat(frames).sort_values(by='date', ascending=False)
        alldata.to_csv(f'datasets/mp_exp_csv/{mp_name}.csv',index = False)

if __name__ == "__main__":
    
        
    # create all individual csv for ever mp 
    expense = 'row align-items-center text-center pt-1 pb-1'
     
    lastrow =  'row border-bottom align-items-center text-center pt-1 pb-1'
    
    create_csv(expense, lastrow)
    
    #create a combined data set.
    data_path = 'datasets/mp_exp_csv'

    files = os.listdir(data_path)

    #combine all files in the list
    combined_expenses = pd.concat([pd.read_csv(f'datasets/mp_exp_csv/{fi}') for fi in files ])
    #export to csv
    combined_expenses.to_csv( 'datasets/combined_expenses.csv', index=False)
  




