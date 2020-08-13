import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import re
from glob import glob
import os

##################################
###         FUNDING            ###
##################################

funding = pd.DataFrame(columns=['Source', 'Cause Area', 'Organization', 'Amount'])

##################################
###      OPEN PHILANTHROPY     ###
##################################

op_grants = pd.read_csv('./data/openphil_grants.csv')

# Standardize cause area names
# standard names from https://80000hours.org/topic/causes/
subs = {
  'Potential Risks from Advanced Artificial Intelligence': 'AI',
  'History of Philanthropy': 'Other',
  'Immigration Policy': 'Policy',
  'Macroeconomic Stabilization Policy': 'Policy',
  'Land Use Reform': 'Policy',
  'Criminal Justice Reform': 'Policy',
  'U.S. Policy': 'Policy',
  'Other areas': 'Other',
  'Biosecurity and Pandemic Preparedness': 'Biosecurity',
  'Farm Animal Welfare': 'Animal Welfare',
  'Global Catastrophic Risks': 'Catastrophic Risks',
  'Global Health & Development': 'Global Poverty',
}
op_grants['Cause Area'] = op_grants['Focus Area'].map(subs).fillna(op_grants['Focus Area'])

subs = {
  'Johns Hopkins Center for Health Security': 'JHCHS',
  'Against Malaria Foundation': 'AMF',
  'Georgetown University': 'GU',
}
op_grants['Organization'] = op_grants['Organization Name'].map(subs).fillna(op_grants['Organization Name'])

# Standardise Column Names
op_grants = op_grants[['Organization', 'Cause Area', 'Amount']]
op_grants['Source'] = 'Open Philanthropy'
funding = funding.append(op_grants)

# Parse funding amounts
funding['Amount'] = funding['Amount'].apply(lambda x: int(x[1:].replace(',', '') if type(x)==str else 0)).astype('int')

##################################
###          EA FUNDS          ###
##################################

ea_funds = pd.DataFrame(columns=['Source', 'Cause Area', 'Organization', 'Amount'])

for path in glob('./data/ea_funds/*.txt'):

  # Extract title
  title = os.path.basename(path)
  title = title[:-4]
  title = title.replace('_',' ')
  title = title.title()

  # Get text
  with open(path) as f:
    lines = f.read().split('\n')

  for line in lines:
    pattern = '\$([\d,.]+) \- ([ \w\d])+: ([ \w]+)'
    amount, date, org = re.match(pattern, line).groups()
  ea_funds.loc[len(ea_funds)] = [
    'EA Funds',
    title,
    org,
    int(amount[:-3].replace(',',''))
  ]

ea_funds['Cause Area'] = ea_funds['Cause Area'].map({
  'Ea Community': 'Meta',
  'Global Development': 'Global Poverty',
  'Far Future': 'Far Future',
  'Animal Welfare': 'Animal Welfare',
})

funding = pd.concat([ea_funds, funding])

##################################
###  GWWC AND FOUNDERS PLEDGE  ###
##################################

other_df = pd.read_csv('data/misc.csv')

funding = pd.concat([other_df, funding])
##################################
###       SANKEY DIAGRAM       ###
##################################

# Transform table from
#   'OpenPhil', 'Global Poverty', 'AMF', 100
#   'OpenPhil', 'Global Poverty', 'SCI', 80
# to
#   'OpenPhil', 'Global Poverty', 180, 'OpenPhil'
#   'Global Poverty', 'AMF', 100, 'OpenPhil'
#   'Global Poverty', 'SCI', 80, 'OpenPhil'
# That is, sum the contributions of each entity to each other entity.
# Each row represents a connection between two entities.
# The last column will be used for coloring the connections.

funding_long = pd.DataFrame(columns=['From', 'To', 'Amount', 'Source'])

for source, cause in set(zip(
    funding['Source'], 
    funding['Cause Area']
  )):

  source_cause_df = funding[ 
    (funding['Source']==source) & \
    (funding['Cause Area']==cause) 
  ]
  total_funding = source_cause_df['Amount'].sum()
  funding_long.loc[len(funding_long)] = [
    source,
    cause,
    total_funding,
    source
  ]

  other_total = 0
  for org in source_cause_df['Organization'].unique():
    org_df = source_cause_df[ 
      (source_cause_df['Organization']==org)
    ]
    total_funding = org_df['Amount'].sum()
    if total_funding < 3*10**7:
      other_total += total_funding
      continue
    funding_long.loc[len(funding_long)] = [
      cause,
      org,
      total_funding,
      source
    ]
  if other_total > 0:
    funding_long.loc[len(funding_long)] = [
      cause,
      'Others',
      other_total,
      source
    ]

# Get a list of all funding-related entities
entities = set()
for col in ['From', 'To']:
    entities.update(funding_long[col])
entities = list(entities)

# Convert financial inputs and outputs into indices
entity2idx = {x: i for i,x in enumerate(entities)}
froms = list(funding_long['From'].map(entity2idx))
tos = list(funding_long['To'].map(entity2idx))

# Create Sankey diagram
funding_fig = go.Figure(
  data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = entities,
      color = "blue"
    ),
    link = dict(
      source = froms, 
      target = tos,
      value = funding_long['Amount']
    )
  )],
  # config={
  #   'displayModeBar': False,
  # }
)
funding_fig.update_layout(
  margin=dict(l=0, r=0, t=0, b=0),
)

##################################
###           TOTALS           ###
##################################

TOTAL_PLEDGED = 100
TOTAL_DONATED = 1