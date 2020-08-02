# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import re
from glob import glob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##################################
###       DEMOGRAPHICS         ###
##################################

demo_pies = []
for table_name in [
        'age_group', 'diet', 'gender', 'employment', 'ethnicity', 'subject',
        ]:

    path = f"./rp_survey_data/{table_name}.csv"
    demo_table = pd.read_csv(path, sep='\t')
    title = demo_table.columns[0]

    # remove the 'Total' row
    demo_table = demo_table[ ~demo_table[title].isin(['Total', 'Total respondents']) ]
    demo_table['label'] = demo_table[title] + demo_table['Percent']
    # convert '5%' to 5
    demo_table['Percent'] = demo_table['Percent'].apply(lambda x: float(x[:-1]))


    pie_fig = px.pie(demo_table, values='Percent', names=title, title=title)#, hovertext='label')
    # pie_fig.update_trace(hovertemplate=)
    pie_fig.update_traces(hoverinfo='none', textinfo='none')
    pie_fig.update(layout_showlegend=False)
    pie_fig.update_layout(
        margin=dict(l=50, r=0, t=50, b=200),
    )
    this_pie = dcc.Graph(
        id=title, #style={'margin': '0%'},
        figure=pie_fig
    )

    demo_pies.append(this_pie)

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

countries = pd.read_csv('./rp_survey_data/country.csv', sep='\t')
countries = countries[
    ~countries['Country'].isin(['All other stated countries', 'Total respondents'])
]
countries['Responses'] = countries['Responses'].astype('int')
countries.replace({'UK': 'United Kingdom', 'USA': 'United States'}, inplace=True)
gapminder = px.data.gapminder().query("year==2007")
gapminder['Country'] = gapminder['country']
countries = countries.merge(gapminder, on='Country', how='left')
map_fig = px.scatter_geo(countries, locations="iso_alpha", #color="continent",
                     hover_name="Country", 
                     size="Responses",
                     # animation_frame="year",
                     projection="natural earth"
)


app.layout = html.Div(children=[
    html.H1('Effective Altruism Dashboard'),

    # html.Div('''
    #     Dash: A web application framework for Python.
    # '''),
   html.Div([

        html.Div([
            dcc.Graph(
                id='map_fig',
                figure=map_fig
            )
        ], style={'width': '49%', 'float': 'right'}),

        html.Div(demo_pies, style={'columnCount': 2, 'float': 'left', 'padding': '0px 0px 0px 200px',
        'width': '30%', 'display': 'inline-block'}),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)