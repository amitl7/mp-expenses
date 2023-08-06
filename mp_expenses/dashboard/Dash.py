import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

# Read the data into a pandas DataFrame
data = pd.read_csv('datasets/combined_expenses.csv', low_memory=(False))

# Create the Dash application
app = dash.Dash(__name__)

# # Set up the layout
app.layout = html.Div(
    children=[
        html.H1("MP's Expenses", style={'text-align': 'center'}),
        html.Div(
            children=[
                dcc.Dropdown(
                    id='dropdown-type',
                    options=[{'label': t, 'value': t} for t in data['type'].unique()],
                    placeholder='Filter by Type',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown-subtype',
                    placeholder='Filter by Sub Type',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown-name',
                    options=[{'label': n, 'value': n} for n in data['name'].unique()],
                    placeholder='Filter by Name',
                    multi=True
                )
            ],
            style={'width': '30%', 'float': 'left'}
        ),
        html.Div(
            children=[
                dcc.Graph(id='bar-chart')
            ],
            style={'width': '70%', 'display': 'inline-block'}
        ),
        html.Div(id='table-div')
    ]
)


# Callback for updating the sub-type dropdown based on the selected type
@app.callback(
    dash.dependencies.Output('dropdown-subtype', 'options'),
    [dash.dependencies.Input('dropdown-type', 'value')]
)
def update_subtype_dropdown(selected_types):
    if selected_types:
        filtered_data = data[data['type'].isin(selected_types)]
        subtypes = filtered_data['sub_type'].unique()
        return [{'label': st, 'value': st} for st in subtypes]
    else:
        return []


# Callback for updating the table based on the selected type
@app.callback(
    dash.dependencies.Output('table-div', 'children'),
    [dash.dependencies.Input('bar-chart', 'clickData')]
)
def update_table(click_data):
    if click_data:
        selected_type = click_data['points'][0]['x']
        filtered_data = data[data['type'] == selected_type]
        table = html.Table(
            children=[
                html.Tr(
                    children=[
                        html.Th(col) for col in filtered_data.columns
                    ]
                )
            ] + [
                html.Tr(
                    children=[
                        html.Td(str(filtered_data.iloc[i][col])) for col in filtered_data.columns
                    ]
                ) for i in range(len(filtered_data))
            ]
        )
        return table
    else:
        return html.Table()

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
