# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

lightbulb_img_url = 'https://effectivealtruism.nz/wp-content/uploads/2018/02/lightbulblogo-1.png'

heading = html.H1(
    [
        html.Img(
            src = lightbulb_img_url,
            className='lightbulb',
        ),
        html.Div(
            [
                html.Span(
                    'Effective',
                    className = 'effective',
                ),
                html.Span(
                    'Altruism',
                    className = 'altruism',
                ),
            ],
            className='effective-altruism',
        ),
        html.Div(
            [
                html.Span(
                    'Data',
                    className = 'data',
                ),
                html.Span(
                    '.com',
                    className = 'dot-com',
                ),
            ],
            className='data-dot-com',
        ),
    ],
    className='ea-data-dot-com center',
)

def title_section():
    return html.Div(
        html.Div(
            [
                html.Div([
                    # html.P('Welcome to'),
                    heading,
                    html.P(
                        [
                            dcc.Link(
                                "Effective Altruism",
                                href="https://www.effectivealtruism.org/"
                            ),
                            ' is a loose collective of quantitatively-minded philanthropists and do-gooders.',
                        ]
                    ),
                    html.P(
                        'There are several EA organisations which collect data on grants, donors, and pledges.',
                    ),
                    html.P(
                        'This website to aggregates and visualizes that data.',
                    ),
                    html.P(
                        [
                            'Source code is available on ',
                            dcc.Link(
                                "Github",
                                href="https://github.com/hamishhuggard/ea_data_viz"
                            ),
                            '.',
                        ]
                    ),
                    html.P(
                        [
                            'Please send feedback to ',
                            dcc.Link(
                                "hamish.huggard@gmail.com",
                                href="mailto:hamish.huggard@gmail.com"
                            ),
                            '.',
                        ],
                    ),
                    html.H3(
                        'Scroll down to see some data...'
                    ),
                ]),
            ],
            className='section-body center',
        ),
        className='section',
    )
