import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.ea_bar_graph import EABarGraph
from countryinfo import CountryInfo
from math import log

##################################
###         WORLD MAP          ###
##################################

# source: https://plotly.com/python/bubble-maps/

country = CountryInfo()
country_list = country.all().keys()

countries = pd.read_csv('./data/rp_survey_data/country2.csv')

countries['Responses'] = countries['Responses'].astype('int')

countries.loc[countries['Country']=='United States of America', 'Country'] = 'United States'

MINIMUM_CIRCLE_SIZE = 0 # 20
countries['circle size'] = countries['Responses'] + MINIMUM_CIRCLE_SIZE

countries = countries.sort_values('Responses', ascending=True)

def get_population(country):
    try:
        return CountryInfo(country).population()
    except:
        return 1e9

countries['population'] = countries['Country'].apply(get_population)
countries['Density (per million)'] = countries['Responses'] / countries['population'] * 1e6
countries['Density (per million)'] = countries['Density (per million)'].apply(lambda x: round(x, 2))
countries['log density'] = countries['Density (per million)'].apply(lambda x: 1 + log(x+1))

countries_for_map = countries.copy()
for country in country_list:
    if country in [ c.lower() for c in countries['Country'] ]:
        continue
    i = len(countries_for_map)
    countries_for_map.loc[i, ['Country', 'Responses', 'Density (per million)', 'log density']] = (country, 0, 0, 0)

# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo.html
map_fig = px.choropleth(
    countries_for_map,
    locations="Country",
    hover_name="Country",
    # hover_data=['Country', 'Responses'],
    locationmode='country names',
    # size="Responses",
    # size="circle size",
    # color='Density (per million)',
    color='log density',
    # color='density plus',
    color_continuous_scale=["#dfe3ee", "#007a8f"],
    hover_data = {
        'circle size': False,
        'Responses': True,
        'Country': False,
        'log density': False,
        'Density (per million)': True,
    },
    projection="equirectangular", # 'orthographic' is fun
    # height=250,
)

map_fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_showscale=False,
)

# map_fig.update_traces(
#     marker = dict(
#         color ="#36859A",
#     ),
# )

map_fig.update_geos(
    showcoastlines=False, 
    # showland=True, 
    # landcolor="#B8C8D3",
    # landcolor="#ffffff",
    # marker_line_color='white',
    landcolor="#dfe3ee",
)

countries['x'] = countries['Country']
countries['text'] = countries['Responses'].apply(lambda x: f'{x:}')
countries['y'] = countries['Responses']

countries_bar = EABarGraph(
    countries,
    height = 23*len(countries),
    title = 'Number of EAs'
)

countries_capita_sort = countries.sort_values(by='Density (per million)')
countries_capita_sort['x'] = countries_capita_sort['Country']
countries_capita_sort['y'] = countries_capita_sort['Density (per million)']
countries_capita_sort['text'] = countries_capita_sort['Density (per million)'].apply(lambda x: f'{x:.1f}')

per_capita_bar = EABarGraph(
    countries_capita_sort,
    height = 23*len(countries),
    title = 'EAs per Million People'
)

class Geography(html.Div):
    def __init__(self):
        super(Geography, self).__init__(
            [
                html.Div(
                    html.H2('Countries'),
                    className='section-heading',
                ),
                html.P([
                    'Data source: ',
                    dcc.Link(
                        '2019 Rethink Priorities Survey',
                        href='https://www.rethinkpriorities.org/blog/2019/12/5/ea-survey-2019-series-community-demographics-amp-characteristics'
                    ),
                ]),
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                id='map_fig',
                                figure=map_fig
                            ),
                            className='map-container'
                        ),
                        html.Div(
                            [
                                html.Div(
                                   countries_bar,
                                   className='countries-bar'
                                ),
                                html.Div(
                                   per_capita_bar,
                                   className='countries-bar'
                                ),
                            ],
                            className = 'countries-bar-container',
                        ),
                    ],
                    className = 'countries-container',
                ),
            ],
            className = 'section',
        )
