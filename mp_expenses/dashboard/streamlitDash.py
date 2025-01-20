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
major_parties = ['Conservative', 'Labour', 'Scottish National Party', 'Liberal Democrats', 'Others']
@st.cache_data
def load_data(location):
    
    df = pd.read_csv(location)
    df['id'] = df['id'].astype(str)
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['amount'] = df['amount'].str.replace(',','')
    df['amount'] = df['amount'].astype(float)

    return df
##combine map and data together
@st.cache_data
def alldata():
    alldata = pd.merge(left = load_data(abs_path), right = mp_map, left_on= 'name', right_on= 'name')
    alldata['party'] = alldata['party_group'].apply(lambda x: x if x in major_parties[:4] else 'Others')
    return alldata


# Sidebar
st.sidebar.title("Filters")

if st.sidebar.button("Clear All Filters"):
    # Reset all selectboxes to "All" using session state
    st.session_state.party = "All"
    st.session_state.type = "All"
    st.session_state.sub_type = "All"
    # Rerun the app to apply the reset
    st.rerun()

party = ["All"] + sorted(alldata()['party'].unique().tolist())
selected_party = st.sidebar.selectbox("Select Constituency", party, index=0)

type = ["All"] + sorted(alldata()['type'].unique().tolist())
selected_type = st.sidebar.selectbox("Select Category", type, index=0)

sub_type = ["All"] + sorted(alldata()['sub_type'].unique().tolist())
selected_subtype= st.sidebar.selectbox("Select Sub Type", sub_type, index=0)

# Modify the filtering logic to only filter when not "All"
filtered_df = alldata().copy()    

if selected_party != "All":
    filtered_df = filtered_df[filtered_df['party'] == selected_party]
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]
if selected_subtype != "All":
    filtered_df = filtered_df[filtered_df['sub_type'] == selected_subtype]


# Main area
st.title("MP Expenses Claimed")
st.subheader("Spending Trends by Political Parties")

# Group by year and party
party_year_spending = (alldata()
                      .groupby(['year', 'party'])['amount']
                      .sum()
                      .reset_index())

type_year_spending = (alldata()
                      .groupby(['type', 'year'])['amount']
                      .sum()
                      .reset_index())

miscellaneous_year_spending = (alldata()
                        .query('type == "Miscellaneous Expenses"')
                        .groupby(['sub_type', 'year'])['amount']
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

fig = px.bar(type_year_spending, x='year', y='amount', color='type',
             labels={'type': 'Subcategory', 'amount': 'Amount GBP'},
             title="Expenses by Type")

def year_spending(df):

    yearly_totals = df.groupby('year')['amount'].sum().round(0)
    yearly_totals_millions = yearly_totals / 1_000_000
    year = df['year'].unique()
    return yearly_totals_millions, yearly_totals, year

# Add annotations for yearly totals
yearly_totals = year_spending(type_year_spending)[1]

for year in yearly_totals.index:
    fig.add_annotation(
        x=year,
        y=yearly_totals[year],  # Using yearly_totals instead of millions
        text=f'£{year_spending(type_year_spending)[0][year]:,.0f}M',  # Format with commas, no 'M' suffix
        showarrow=False,
        yshift=10,
        font=dict(size=12, weight='bold')
    )

# Customize the layout
fig.update_layout(
    barmode='stack',
    xaxis_tickangle=0,
    legend_title_text='Subcategory',
    showlegend=True,
    yaxis_title='Amount GBP',
    xaxis_title='Year',
    xaxis=dict(
        tickmode='array',
        tickvals=year_spending(type_year_spending)[2],  # Show all years
        dtick=1  # Force display of each year
    )
)

# Add hover template
fig.update_traces(
    hovertemplate="<br>".join([
        "Year: %{x}",
        "Amount: £%{y:,.0f}",
        "Category: %{customdata}<br>"
    ]),
    customdata=type_year_spending['type']
)

st.plotly_chart(fig)

miscellanous_fig = px.bar(miscellaneous_year_spending, x='year', y='amount', color='sub_type',
             labels={'sub_type': 'Sub type', 'amount': 'Amount GBP'},
             title="Miscellaneous Expenses by Subcategory")

yearly_totals = year_spending(miscellaneous_year_spending)[1]

for year in yearly_totals.index:
    miscellanous_fig.add_annotation(
        x=year,
        y=yearly_totals[year],  # Using yearly_totals instead of millions
        text=f'£{(year_spending(miscellaneous_year_spending)[1])[year]:,.0f}k',  # Format with commas, no 'M' suffix
        showarrow=False,
        yshift=10,
        font=dict(size=12, weight='bold')
    )

miscellanous_fig.update_layout(
    barmode='stack',
    xaxis_tickangle=0,
    legend_title_text='Miscellaneous details',
    showlegend=True,
    yaxis_title='Amount GBP',
    xaxis_title='Year',
    xaxis=dict(
        tickmode='array',
        tickvals=year_spending(miscellaneous_year_spending)[2],  # Show all years
        dtick=1  # Force display of each year
    )
)

# Add hover template
miscellanous_fig.update_traces(
    hovertemplate="<br>".join([
        "Year: %{x}",
        "Amount: £%{y:,.0f}",
        "Category: %{customdata}<br>"
    ]),
    customdata=miscellaneous_year_spending['sub_type']
)

st.plotly_chart(miscellanous_fig)


# Data Table
st.subheader("Data Table")
st.write(filtered_df)
