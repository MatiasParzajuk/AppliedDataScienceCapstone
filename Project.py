import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app = dash.Dash(__name__)

min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
        {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
]

app.layout = html.Div([
        html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

        html.Label("Select Launch Site:"),
        dcc.Dropdown(
                id='site-dropdown',
                options=site_options,
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
        ),

        html.Br(),
        
        html.Label("Select Payload Range (Kg):"),
        dcc.RangeSlider(
                id='payload-slider',
                min=0,
                max=10000,
                step=1000,
                value=[min_payload, max_payload],
                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}
        ),
        
        html.Br(),
        dcc.Graph(id='success-pie-chart'),
        dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(
        Output('success-pie-chart', 'figure'),
        Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):
        if entered_site == 'ALL':
                df_all = spacex_df[spacex_df['class'] == 1]
                fig = px.pie(
                        df_all,
                        names='Launch Site',
                        title='Total Successful Launches by Site'
                )
                return fig
        else:
                df_site = spacex_df[spacex_df['Launch Site'] == entered_site]
                fig = px.pie(
                        df_site,
                        names='class',
                        title=f'Total Success vs. Failure for site {entered_site}',
                        color='class',
                        color_discrete_map={0: 'blue', 1: 'red'},
                        category_orders={'class': [1, 0]}
                )
                fig.update_traces(
                        textinfo='percent+label'
                )
                return fig
        
@app.callback(
        Output('success-payload-scatter-chart', 'figure'),
        [
                Input('site-dropdown', 'value'),
                Input('payload-slider', 'value')
        ]
)
def get_scatter_chart(selected_site, payload_range):
        low, high = payload_range

        filtered_df = spacex_df[
                (spacex_df['Payload Mass (kg)'] >= low) &
                (spacex_df['Payload Mass (kg)'] <= high)
        ]
        if selected_site == 'ALL':
                fig = px.scatter(
                        filtered_df,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for All Sites',
                        hover_data=['Launch Site']
                )
                return fig
        else:
                filtered_site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
                fig = px.scatter(
                        filtered_site_df,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version Category',
                        title=f'Correlation between Payload and Success for {selected_site}',
                        hover_data=['Launch Site']
                )
                return fig

if __name__ == '__main__':
        app.run(debug=True, port=8050)