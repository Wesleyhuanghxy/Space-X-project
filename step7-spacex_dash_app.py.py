# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for the pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    print(f"Selected site for pie chart: {selected_site}")
    if selected_site == 'ALL':
        print("Pie chart: Displaying all sites")
        print(spacex_df['Launch Site'].value_counts())
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        print(f"Pie chart data for {selected_site}:")
        print(filtered_df['class'].value_counts())
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for site {selected_site}'
        )
    return fig

# TASK 4: Callback for the scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    print(f"Payload range selected: {payload_range}")
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    print(f"Filtered data based on payload range ({payload_range}):")
    print(filtered_df.head())
    
    if selected_site == 'ALL':
        print("Scatter plot: Displaying all sites")
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title='Payload vs Success for All Sites'
        )
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        print(f"Scatter plot data for {selected_site}:")
        print(site_filtered_df.head())
        fig = px.scatter(
            site_filtered_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title=f'Payload vs Success for site {selected_site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
