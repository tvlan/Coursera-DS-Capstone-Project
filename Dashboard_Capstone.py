# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

list1 = range(0,10001,1000)
list2 = [i+'kg'for i in list(map(str,list1))]
list3 = dict(zip(list1,list2))

count_sites = spacex_df.groupby('Launch Site', as_index = False).count()
Test = count_sites['Launch Site']
print(Test)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                              options = [{'label' :'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                        {'label' :'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                        {'label' :'KSC LC-39A', 'value':'KSC LC-39A'},
                                                        {'label' :'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                        {'label' :'ALL', 'value':'ALL'},],
                                                value = 'ALL',
                                                        
                                              
                                    
                                              placeholder="Launch Sites",
                                              searchable=True,
                                              

                                              ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(0,10000,1000,id='payload-slider',marks = list3 , value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
@app.callback( Output('success-pie-chart' , 'Figure'  ),
           Input('site-dropdown' , 'value'))
def get_pie_chart( entered_site):
    filtered_df = spacex_df[spacex_df['class']==1]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df ,
        names = 'Launch Site',
        title = 'Successfull Launches at All Sites')
        return fig
    else:
            print(f'Running for site: {entered_site}')
            filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
            fig = px.pie(filtered_df, names='class', title=f'Success Rate for {entered_site}')
            print(f'Pie chart generated successfully for {entered_site}.')
            return fig

    
    
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
            Input(component_id='payload-slider',component_property='value'),
            Input(component_id ='site-dropdown',component_property='value'))
def get_scatter(payload_slider,drop_input):
        if drop_input == 'ALL':
            filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
            &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
            fig_2 = px.scatter(filtered_data , x='Payload Mass (kg)' , y='Launch Site',color="Booster Version Category")
            print('running')
            return fig_2
        else:
            specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
            filtered_data = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])
            &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
            fig_2 = px.scatter(spacex_df, x='Payload Mass (kg)' , y='Launch Site',color="Booster Version Category")
            print('running')
            return fig_2


# Run the app
if __name__ == '__main__':
    app.run_server()
