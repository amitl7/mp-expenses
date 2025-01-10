#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:08:22 2021

@author: amitlandge
streamlit run "/Users/amitlandge/Box Sync/code/mp_expenses/main.py"
"""
#from pandas.core.indexes.base import Index
import streamlit as st
# Set page config must be the first st command
st.set_page_config(page_title="MP Expenses Dashboard", layout="wide")

# Import other libraries
import pandas as pd
import altair as alt
import os
import plotly.express as px

# Get the directory of the current script
current_dir = os.getcwd()
print(f"Current Directory: {current_dir}")

# Get the parent directory
parent_dir = os.path.dirname(current_dir)
print(f"Parent Directory: {parent_dir}")

csv_path = os.path.join(parent_dir, 'datasets', 'combined_expenses.csv')
print("CSV Path:", csv_path)
abs_path = '/Users/amitlandge/Library/CloudStorage/Box-Box/code/mp-expenses/mp_expenses/datasets/combined_expenses.csv'



mp_map = pd.read_csv('/Users/amitlandge/Library/CloudStorage/Box-Box/code/mp-expenses/mp_expenses/datasets/mp_map.csv')

@st.cache_data
def load_data(location):
    df = pd.read_csv(location)
    return df

combined_expenses = load_data(abs_path)
combined_expenses['id'] = combined_expenses['id'].astype(str)
combined_expenses['year'] = pd.DatetimeIndex(combined_expenses['date']).year
combined_expenses['amount'] = combined_expenses['amount'].str.replace(',','')
combined_expenses['amount'] = combined_expenses['amount'].astype(float)


##combine map and data together
alldata = pd.merge(left = combined_expenses, right = mp_map, left_on= 'name', right_on= 'name')
# aggregate data
byparty = alldata.groupby(['year','party'])['amount'].sum()
#### need to edit all below variables
# Set up page configuration


# Sidebar
st.sidebar.title("Filters")

party = ["All"] + sorted(alldata['party'].unique().tolist())
selected_party = st.sidebar.selectbox("Select Constituency", party, index=0)

type = ["All"] + sorted(alldata['type'].unique().tolist())
selected_type = st.sidebar.selectbox("Select Category", type, index=0)

sub_type = ["All"] + sorted(alldata['sub_type'].unique().tolist())
selected_subtype= st.sidebar.selectbox("Select Sub Type", sub_type, index=0)

# Modify the filtering logic to only filter when not "All"
filtered_df = alldata.copy()

if selected_party != "All":
    filtered_df = filtered_df[filtered_df['party'] == selected_party]
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]
if selected_subtype != "All":
    filtered_df = filtered_df[filtered_df['sub_type'] == selected_subtype]


# Main area
st.title("MP Expenses Claimed")
st.subheader("Spending Trends by Political Parties")

# Define the major parties we want to show
major_parties = ['Conservative', 'Labour', 'Scottish National Party', 'Liberal Democrats', 'Others']

# Create a copy of filtered_df and modify the party column
party_data = filtered_df.copy()
# Replace all other parties with 'Others'
party_data['party'] = party_data['party'].apply(lambda x: x if x in major_parties[:4] else 'Others')

# Group by year and party
party_year_spending = (party_data
                      .groupby(['year', 'party'])['amount']
                      .sum()
                      .reset_index())

# Create the stacked area chart
party_trend_fig = px.area(party_year_spending, 
                         x='year', 
                         y='amount',
                         color='party',
                         title='Spending Trends by Political Parties',
                         labels={'year': 'Year',
                                'amount': 'Total Amount (£)',
                                'party': 'Political Party'},
                         height=500,
                         # Set custom color scheme
                         color_discrete_map={
                             'Conservative': '#0087DC',    # Conservative blue
                             'Labour': '#DC241F',          # Labour red
                             'Scottish National Party': '#FDF38E',  # SNP yellow
                             'Liberal Democrats': '#FDBB30',  # Lib Dem orange
                             'Others': '#808080'           # Grey for others
                         },
                         category_orders={"party": major_parties})  # Force order in legend

# Customize the layout
party_trend_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Total Amount (£)",
    showlegend=True,
    legend_title="Political Parties",
    xaxis=dict(
        tickmode='linear',
        dtick=1
    )
)

# Update line and fill properties
party_trend_fig.update_traces(
    mode='lines',
    line=dict(width=2),
    stackgroup='one'
)

# Display the chart
st.plotly_chart(party_trend_fig, use_container_width=True)
# Bar Chart
st.subheader("Expenses Overview")
fig = px.bar(filtered_df, x='sub_type', y='amount', color='sub_type',
             labels={'sub_type': 'Subcategory', 'amount': 'Amount'},
             title="Expenses by Subcategory")
st.plotly_chart(fig)

# Data Table
st.subheader("Data Table")
st.write(filtered_df)
