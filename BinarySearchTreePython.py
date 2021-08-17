# imports
import csv
import json
import dash
import pandas as pd
import sys, getopt, pprint, os
import pymongo
import numpy as np
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import dash_table as dt
import base64
from pprint import pprint
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient
from dash.dependencies import Input, Output, State
from dbCRUD import BidSystem

##### THIS SECTION ONLY NEEDED FOR INITIAL SETUP #####
# Setup to import the csv file into mongodb through mongodb atlas
#def import_content(filepath):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
#    client = pymongo.MongoClient("mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority")
    # details for the database and collection names
#    mng_db = client['mongodb_eBids']
#    collection_name = 'eBids'
#    db_cm = mng_db[collection_name]
    # setup to pull the data from csv file and insert into mongodb as json data
#    cdir = os.path.dirname(__file__)
#    file_res = os.path.join(cdir, filepath)
#    data = pd.read_csv(file_res)
#    data_json = json.loads(data.to_json(orient='records'))
#    db_cm.remove()
#    db_cm.insert(data_json)

#if __name__ == "__main__":
#    filepath = 'eBids.csv'
#    import_content(filepath)
###### THIS SECTION ONLY NEEDED FOR INITIAL SETUP #####

###########################
# Data Manipulation / Model
###########################
ebids = BidSystem()

# class read method must support return of cursor object 
df = pd.DataFrame.from_records(ebids.read({}))

#########################
# Dashboard Layout / View
#########################
app = dash.Dash()
server = app.server

# Auction logo
image_filename = 'AuctionHousePicture.jpg'
## image source: httpweknowyourdreams.comsingleauctionauction-08
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#App HTML layout
app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.A([
            html.Img(
                src= 'data:image/png;base64,{}'.format(encoded_image.decode()),
                style={
                    'height' : '25%',
                    'width' : '25%',
                    'float' : 'left',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
                })
    ], href='https://www.snhu.edu'),
    html.Br(),
    html.Hr(),
    html.Center(html.B(html.H1('Daniel Ostrin Capstone Project'))),
    html.Hr(),
#Dropdown selection
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            #{'label': '', 'value': ''},
            ### was going to add more drop downs for quicker sorting but ran out of time.
        ],
        value='All'
    ),
#datatable Options
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        #features for your interactive data table to make it user-friendly
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable="single",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current = 0,
        page_size= 10,
        ),
    html.Hr(),
    html.Div(id='output'),
    html.Br(),
    html.Hr(),
#This sets up the dashboard for the pie chart",
    html.Div(className='row',
        style={'display' : 'flex'},
        children=[
        html.Div(
            dcc.Graph(id='the_graph'),
            id='graph-id',
            className='col s12 m6',
         
            ),
        
        ]),
    html.Br(),
    html.Hr(),
    html.Header("Daniel Ostrin Capstone Project")
    
    ])
    

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('demo-dropdown', 'value')])
def update_dashboard(value):
###filter interactive data table with MongoDB queries
    if (value == 'All'):
        df = pd.DataFrame.from_records(ebids.read({}))
   
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
        
        
    return (data,columns)

#callback that controls the color of selected item
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

#Callback to show which row was deleted (trying to use to trigger a delete)
@app.callback(Output('output', 'children'),
              [Input('datatable-id', 'data_previous')],
              [State('datatable-id', 'data')])
def show_removed_rows(previous, current):
    if previous is None:
        dash.exceptions.PreventUpdate()
    else:
        return [f'Just removed {row}' for row in previous if row not in current]
    #[f'Just removed {row}' for row in previous if row not in current] 
    #items.delete(items, row)

#Callback for the pie chart
@app.callback(
    Output('the_graph', "figure"),
    [Input('datatable-id', "derived_viewport_data")])
def update_graph(viewData):
    dff = pd.DataFrame.from_dict(viewData)

    piechart = px.pie(data_frame = dff,
                      values = 'Auction Id',
                      names = 'Department ')    
    return (piechart)

if __name__ == "__main__":
    app.run_server(debug=True)
