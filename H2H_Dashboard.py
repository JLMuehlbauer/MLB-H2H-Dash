#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 19:39:22 2023

@author: jacksonmuehlbauer
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup as bs


teams = [
    "ARI", "ATL", "BAL", "BOS", "CHC", "CIN", "CLE", "COL", "CWS", "DET",
    "HOU", "KC", "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "OAK",
    "PHI", "PIT", "SD", "SEA", "SF", "STL", "TB", "TEX", "TOR", "WSH"
]

# Function to grab players on team
def get_players_on_team(team, year, player_type):
    """
    team : str, 3 Character Name of Team
    year : int, ex. 2021
    player_type : str, "batting" or "pitching"
    return dataframe
    """
    
    records = []
    url = f'https://www.baseball-reference.com/teams/{team}/{year}.shtml'
    page = requests.get(url)
    soup = bs(page.content,"html.parser")    
    table = soup.find(id=f"all_team_{player_type}")
    tab_text = table.decode_contents().split('tbody')[1].strip()
    tab_soup = bs(tab_text,"html.parser")

    # extracting records from table
    for i, row in enumerate(tab_soup.find_all('tr')):
        record = {}
        for col in row.find_all('td'):
            name = str(col).split('data-stat')[1].split('"')[1]
            value = col.text.strip()
            record[name] = value
        if record != {}:
            records.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame.from_records(records)
    
    if player_type == "batting":
        df['PA'] = df['PA'].apply(pd.to_numeric, errors='coerce')
        df = df.query('PA > 30').copy()
    elif player_type == "pitching":
        df['IP'] = df['IP'].apply(pd.to_numeric, errors='coerce')
        df = df.query('IP > 10').copy()
        df.drop(columns = 'win_loss_perc', inplace = True)
    
    # Clean
    coercible_columns = df.columns[df.apply(lambda x: pd.to_numeric(x, errors='coerce').notna()).all()]
    # Convert coercible columns to numeric
    df[coercible_columns] = df[coercible_columns].apply(pd.to_numeric, errors='coerce')
    df.reset_index(inplace = True)
    df['team_yr'] = f'{team} {year}'
    
    return df
    
  

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("MLB Head to Head"),
    
    # Dropdown for selecting team 1
    dcc.Dropdown(
        id='team1-selector',
        options= teams,
        multi = False,
        value= teams[0]
    ),
    # Input for selecting year for team 1
    dcc.Input(id='team1year-input', type='number', value= 2023),
    
    # Dropdown for selecting team 2
    dcc.Dropdown(
        id='team2-selector',
        options= teams,
        multi = False,
        value=teams[1]
    ),
    # Input for selecting year for team 2
    dcc.Input(id='team2year-input', type='number', value= 2023),
    
    # Scatter plot component
    dcc.Graph(id='scatter-plot'),
])

# Define callback to update the scatter plot based on dropdown selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('team1-selector', 'value'),
     Input('team1year-input', 'value'),
     Input('team2-selector', 'value'),
     Input('team2year-input', 'value')]
)


def update_scatter_plot(team1, team1year, team2, team2year):
    if team1:
        bat_data1 = get_players_on_team(team1, team1year, 'batting')
        pitch_data1 = get_players_on_team(team1, team1year, 'pitching')
    if team2:
        bat_data2 = get_players_on_team(team2, team2year, 'batting')
        pitch_data2 = get_players_on_team(team2, team2year, 'pitching')

    bat = pd.concat([bat_data1, bat_data2], axis = 0)
    pitch = pd.concat([pitch_data1, pitch_data2], axis = 0)
    SP = pitch.loc[pitch['pos'] == 'SP', :]
    RP = pitch.loc[pitch['pos'] != 'SP', :]
    
    fig = make_subplots(rows=2, cols=4, 
                        vertical_spacing=0.06,
                        subplot_titles=("Batting Average", 
                                        "OBP", 
                                        "Slugging", 
                                        "Runs Scored", 
                                        "ERA", 
                                        "WHIP", 
                                        "K/BB", 
                                        "Runs Allowed"))
    
    bat_hover = [f'{player} \n AB:{ip}' for player, ip in zip(list(bat['player'].values), list(bat['AB'].values))]
    SP_hover = [f'{player} \n IP:{ip}' for player, ip in zip(list(SP['player'].values), list(SP['IP'].values))]
    RP_hover = [f'{player} \n IP:{ip}' for player, ip in zip(list(RP['player'].values), list(RP['IP'].values))]
    
    # Batting Average 
    fig.add_trace(
        go.Scatter(
                   x = bat['team_yr'],
                   y = bat['batting_avg'],
                   mode='markers',
                   marker=dict(
                       size=bat['AB'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=8,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = bat_hover,
                   name='Batting Average'),
        row=1, col=1
    )

    # OBP
    fig.add_trace(
        go.Scatter(
                   x = bat['team_yr'],
                   y = bat['onbase_perc'],
                   mode='markers',
                   marker=dict(
                       size=bat['AB'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=8,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = bat_hover,
                   name='OBP'),
        row=1, col=2
    )
    
    # Slugging
    fig.add_trace(
        go.Scatter(
                   x = bat['team_yr'],
                   y = bat['slugging_perc'],
                   mode='markers',
                   marker=dict(
                       size=bat['AB'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=8,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = bat_hover,
                   name='Slugging'),
        row=1, col=3
    )
    
    # Runs Scored
    fig.add_trace(
        go.Bar(
               x = bat['team_yr'],
               y = bat['R'],
               marker = dict(color = 'blue'),
               hovertext = bat_hover,
               name = 'Runs Scored'
    ),
    row=1, col=4
    )


    # ERA
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] == 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] == 'SP', 'earned_run_avg'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] == 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = SP_hover,
                   name='SP ERA'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] != 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] != 'SP', 'earned_run_avg'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] != 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='red',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = RP_hover,
                   name='RP ERA'),
        row=2, col=1
    )
    
    # WHIP
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] == 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] == 'SP', 'whip'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] == 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = SP_hover,
                   name='SP WHIP'),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] != 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] != 'SP', 'whip'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] != 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='red',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = RP_hover,
                   name='RP WHIP'),
        row=2, col=2
    )
    
    
    # K/BB
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] == 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] == 'SP', 'strikeouts_per_base_on_balls'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] == 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='blue',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = SP_hover,
                   name='SP K/BB'
                   ),
        row=2, col=3
    )
    fig.add_trace(
        go.Scatter(
                   x = pitch.loc[pitch['pos'] != 'SP', 'team_yr'],
                   y = pitch.loc[pitch['pos'] != 'SP', 'strikeouts_per_base_on_balls'],
                   mode='markers',
                   marker=dict(
                       size=pitch.loc[pitch['pos'] != 'SP', 'IP'],  # Specify the size of the bubbles
                       sizemode='diameter',  # Size mode can be 'diameter' or 'area'
                       sizeref=2,  # Controls the scaling of bubble sizes
                       color='red',  # Color of the bubbles
                       opacity=0.7  # Opacity of the bubbles
                   ),
                   hovertext = RP_hover,
                   name='RP K/BB'
                   ),
        row=2, col=3
    )
    
    # Runs Scored
    fig.add_trace(
        go.Bar(
               x = SP['team_yr'],
               y = SP['R'],
               marker = dict(color = 'blue'),
               hovertext = SP_hover,
               name = 'SP Runs Allowed'
    ),
    row=2, col=4
    )
    fig.add_trace(
        go.Bar(
               x = RP['team_yr'],
               y = RP['R'],
               marker = dict(color = 'red'),
               hovertext = RP_hover,
               name = 'RP Runs Allowed'
    ),
    row=2, col=4
    )
    
    teams = bat['team_yr'].unique()
    
    fig.update_layout(height=900, title_text= f'{teams[0]} vs. {teams[1]}')
    
    
    '''
    fig = px.scatter(
        data,
        x='team',
        y='batting_avg',
        size = 'AB',
        color = 'team',
        title='Batting Average',
        hover_data = ['player', 'pos']
    
    )'''
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)