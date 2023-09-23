#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:46:53 2023

@author: jacksonmuehlbauer
"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

# Sample data
x = ['LAD', 'BOS']
y = [10, 11]
#sizes = [30, 40, 50, 60, 70]  # Size of the bubbles

# Create a bubble plot
fig = go.Figure()

# Add a scatter trace with mode='markers' for the bubble plot
fig.add_trace(go.Bar(
    x=x,
    y=y,

    ))

# Set axis labels and chart title
fig.update_layout(
    xaxis_title='X-Axis',
    yaxis_title='Y-Axis',
    title='Bubble Plot Example'
)



# Show the figure
fig.show()

