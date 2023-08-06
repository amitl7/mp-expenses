#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:08:22 2021

@author: amitlandge
streamlit run "/Users/amitlandge/Box Sync/code/mp_expenses/main.py"
"""
#from pandas.core.indexes.base import Index
import streamlit as st
import pandas as pd
import altair as alt

#''' altair encodings for graphs https://altair-viz.github.io/user_guide/encoding.html '''

### import all of the data
combined_expenses = pd.read_csv('datasets/combined_expenses.csv', low_memory=(False))
combined_expenses['id'] = combined_expenses['id'].astype(str)
combined_expenses['year'] = pd.DatetimeIndex(combined_expenses['date']).year

mp_map = pd.read_csv('datasets/mp_map.csv')
###  ----------------------
combined_expenses['amount'] = combined_expenses['amount'].str.replace(',','')
combined_expenses['amount'] = combined_expenses['amount'].astype(float)
combined_expenses['year'] = pd.DatetimeIndex(combined_expenses['date']).year

##combine map and data together
alldata = pd.merge(left = combined_expenses, right = mp_map, left_on= 'name', right_on= 'name')
# aggregate data
byparty = alldata.groupby(['year','party'])['amount'].sum()

def main():
    st.title('Mp Expenses Visualised')

    ### ------ sidebar ------
    st.sidebar.title("Select options")

    option = st.sidebar.selectbox("Select View", ('Overall Summary','By party','By MP'))
    st.header(option)

    if option == 'Overall Summary': 
        overall_summary()

### ------ PAGES ------

def overall_summary():   
    years = alldata.year.unique()
    unique_years = st.sidebar.selectbox("Select Year", years)
    st.write('hi')

    byparty = alldata.groupby(['year','party'], as_index = False)['amount'].sum()
    partylist = ['Conservative', 'Labour','Liberal Democrat','Green Party','Scottish National Party']
    byparty['Aggregateparty'] = byparty.party.map( lambda x: x if x in partylist else 'Other')

    chart = alt.Chart(byparty.reset_index()
 #                      ).transform_fold(partynames).mark_line().encode( 
#transform_fold is used to convert between long form and wide form data https://altair-viz.github.io/user_guide/data.html#data-long-vs-wide
                    ).mark_bar().encode(
            alt.X('year:O'),
            alt.Y('amount:Q'),
            color='Aggregateparty:N',
        ).interactive()
    
  

    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
