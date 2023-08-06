#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 21:08:15 2021

@author: amitlandge
"""
#import lxml
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import os

def get_mp_info():
    
    with open('MPs.html', 'r') as html_file:
        content = html_file.read()
        
        
        soup = BeautifulSoup(content, 'lxml')
    
        mp_info = soup.find_all('div', class_= 'card-body pt-0 pb-0 pl-0')
        
        data={'name':[], 
              'party':[],
              'location':[],
              'cabinet':[]
              
              }
        
        weblink= {
            'name':[],
            'expenses_link':[]
            }
        
        for info in mp_info:
            
            mp_name = info.h3.text
            data['name'].append(mp_name)
            
            
            party = info.h6.text.split('-')[0]
            party = party.strip()
            data['party'].append(party)
            
            location = info.h6.text.split('-')[1:]
            location = str(location).replace('\n','').replace('[','').replace(']','').replace("'",'')
            data['location'].append(location)
    
            mp_cabinet = info.find('div', class_= 'col-sm-4').text.strip()
            data['cabinet'].append(mp_cabinet)
            
            weblink['name'].append(mp_name)
            
            
            mpnamelink = mp_name.replace(' ','-')
            url = (link+'/mp/'+mpnamelink+'/expenses')
            weblink['expenses_link'].append(url)
            
      
            
        df = pd.DataFrame(data)
        #dataclean
        df.location = [i.replace('\\n','').replace(',  ','').strip().split('     ') for i in df.location]

        df.location = [max(i , key = len) for i in df.location ]

        df.party = [i.replace('(Co','') for i in df.party]
        df['party'] = [i.strip() for i in df['party']]
        
        
        dict_party = {
            'Conservative' :'Conservative',
            'Labour':'Labour',
            'Scottish National Party':'Scottish National Party',
            'Liberal Democrat':'Liberal Democrat',
            'Others': ['Democratic Unionist Party', 'Sinn Féin', 'Independent', 'Plaid Cymru'
 'Alba Party', 'Social Democratic & Labour Party', 'Green Party', 'Alliance',
 'Speaker']        
                          
        }
        df['party_group'] = df['party'].map(dict_party)
        
        #save data
        df.to_csv('datasets/mp_map.csv', index = False)
        print(df.head())
        print ('saved mp_map')
        
        weblinks = pd.DataFrame(weblink)
        weblinks.to_csv('datasets/weblinks.csv',index = False)
        print('saved weblinks csv')
        #print(df)


def get_html(df):
        
    for index, row in df.iterrows():
        name = row['name']
        webpage= row['expenses_link']
        
        #print (f"this is for {name}")
        
        try:
            urllib.request.urlretrieve(f'{webpage}', f'datasets/mp_exp_html/{name}.html')
        
        except:
            print(f"{name} not loaded")


#constants
link = 'https://www.parallelparliament.co.uk'
mp_exp_html = '/datasets/mp_expense_claim/'
mp_weblinks = pd.read_csv('datasets/weblinks.csv')

#run fuctions 

#get_html(mp_weblinks)
get_mp_info()    