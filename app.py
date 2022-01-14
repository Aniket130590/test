import flask; import plotly.express as px
import dash; import dash_core_components as dcc; import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


#Load csv data 
df = pd.read_csv('gimnasio.csv') 
df = df.drop(columns=['Unnamed: 0', 'mes.1', 'mes.2', 'mes.3', 'mes.4'])
df['date']=pd.to_datetime(df['date'])
available_indicators = df.columns.unique()

#Dash code
app.layout = html.Div([
    html.Div([html.H1('GYM VS. ECONOMY' ,
            style={
            'textAlign': 'center', 'font-family': 'Open Sans',
            'padding-top':'10px', 'font-weight': '600', 
            'word-spacing': '5px'
        }),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Intensity_economia'
        )
        ],
        style={'width': '45%', 'display': 'inline-block', 'padding': '15px',
               'font-family': 'Open Sans'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Intensity_gimnasio'
        )
        ], 
        style={'width': '45%', 'float': 'right', 'display': 'inline-block', 
                  'padding': '15px', 'font-family': 'Open Sans'})
    ]),
        html.Div([
        dcc.Graph(
            id='indicator-graphic'
        )
        ], 
        style={'width':'96%', 'height': '60%', 'display': 'inline-block', 'padding': '15px'}),
        
        html.Div([
        dcc.Graph(id='x-time-series'
        )
        ], 
        style={'width': '46%', 'display': 'inline-block', 'padding': '15px'}),
  
        html.Div([
        dcc.Graph(id='y-time-series'
        )
        ],
        style={'width': '46%', 'display': 'inline-block', 'padding': '15px'})

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')])

def update_graph(xaxis_column, yaxis_column):
    
    fig = px.density_heatmap(df, x=xaxis_column,
                            y=yaxis_column)
    return fig


@app.callback(
    Output('x-time-series', 'figure'),
    [Input('xaxis-column', 'value')])

def update_x_timeseries(xaxis_column):
    
    fig = px.scatter(df, x='date', y=xaxis_column,
                    trendline='lowess', trendline_color_override='crimson')
    return fig


@app.callback(
    Output('y-time-series', 'figure'),
    [Input('yaxis-column', 'value')])

def update_y_timeseries(yaxis_column):
    
    fig = px.scatter(df, x='date', y=yaxis_column,
                    trendline='lowess', trendline_color_override='crimson')
    return fig


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, use_reloader=False)
