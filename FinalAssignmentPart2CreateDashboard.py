#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
# TASK 2.2 (part 1): Fix dropdown options labels and values
dropdown_options = [
    {'label': 'Yearly Statistics',            'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics',  'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

#---------------------------------------------------------------------------------------
# TASK 2.1 + 2.2 + 2.3: Create the layout of the app
app.layout = html.Div([

    # TASK 2.1: Dashboard title with style
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 24,
            'fontFamily': 'Arial, sans-serif'
        }
    ),

    # TASK 2.2: First dropdown – Select report type
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',          # <-- component id
            options=dropdown_options,           # <-- list of options
            value='Select Statistics',          # <-- default value
            placeholder='Select a report type' # <-- placeholder text
        )
    ]),

    # TASK 2.2: Second dropdown – Select year
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select Year',               # <-- default value
            placeholder='Select a year'
        )
    ),

    # TASK 2.3: Division for output display
    html.Div([
        html.Div(
            id='output-container',             # <-- output div id
            className='chart-item',
            style={'display': 'flex', 'flexWrap': 'wrap'}
        ),
    ])
])

#---------------------------------------------------------------------------------------
# TASK 2.4 – Callback 1: Enable/disable the year dropdown
# When "Yearly Statistics" is chosen, year dropdown is enabled (disabled=False).
# For any other choice (e.g. Recession), disable it.
@app.callback(
    Output(component_id='select-year',         component_property='disabled'),
    Input(component_id='dropdown-statistics',  component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False   # year dropdown is ENABLED
    else:
        return True    # year dropdown is DISABLED


#---------------------------------------------------------------------------------------
# TASK 2.4 – Callback 2: Update the charts based on selected statistics & year
@app.callback(
    Output(component_id='output-container',    component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year',         component_property='value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # ------------------------------------------------------------------ #
    # TASK 2.5 – Recession Period Statistics                              #
    # ------------------------------------------------------------------ #
    if selected_statistics == 'Recession Period Statistics':

        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1 – Line chart: Average auto sales by year during recessions
        yearly_rec = (
            recession_data
            .groupby('Year')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2 – Bar chart: Average vehicles sold by vehicle type
        average_sales = (
            recession_data
            .groupby('Vehicle_Type')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type during Recession"
            )
        )

        # Plot 3 – Pie chart: Total advertising expenditure share by vehicle type
        exp_rec = (
            recession_data
            .groupby('Vehicle_Type')['Advertising_Expenditure']
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Expenditure Share by Vehicle Type during Recession"
            )
        )

        # Plot 4 – Bar chart: Effect of unemployment rate on vehicle type & sales
        unemp_data = (
            recession_data
            .groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
            .mean()
            .reset_index()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={'display': 'flex'}
            )
        ]

    # ------------------------------------------------------------------ #
    # TASK 2.6 – Yearly Statistics                                        #
    # ------------------------------------------------------------------ #
    elif input_year and selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Plot 1 – Line chart: Yearly average automobile sales (whole period)
        yas = (
            data
            .groupby('Year')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Average Automobile Sales'
            )
        )

        # Plot 2 – Line chart: Total monthly automobile sales
        mas = (
            data
            .groupby('Month')['Automobile_Sales']
            .sum()
            .reset_index()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3 – Bar chart: Average vehicles sold by vehicle type for the selected year
        avr_vdata = (
            yearly_data
            .groupby('Vehicle_Type')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )

        # Plot 4 – Pie chart: Total advertising expenditure by vehicle type for the selected year
        exp_data = (
            yearly_data
            .groupby('Vehicle_Type')['Advertising_Expenditure']
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle in {}'.format(input_year)
            )
        )

        # TASK 2.6: Return the yearly charts
        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={'display': 'flex'}
            )
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
