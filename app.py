import flask; import plotly.express as px
import dash; import dash_core_components as dcc; import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from fuzzywuzzy import fuzz


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

df=pd.read_csv('consolidated.csv')

df["FirstName"] = df["name"].apply(lambda x: x[0:x.find(",")])
df["LastName"] = df["name"].apply(lambda x: x[x.find(",")+2:])

def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.loc[:,['name','title','citizenships','addresses','source_list_url','source_information_url']]])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.loc[:,['name','title','citizenships','addresses','source_list_url','source_information_url']]
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()
app.layout = html.Div(
    children=[html.H4(children='Denied Party Screening'),
    dcc.Dropdown(
        id='dropdown',
        ## extend the options to consider unique Fund values as well
        #options=[{'label': i, 'value': i} for i in df['Investor'].unique()] + [{'label': i, 'value': i} for i in df['Fund'].unique()],
        options=[{'label': i, 'value': i} for i in df['FirstName'].unique()] + [{'label': i, 'value': i} for i in df['LastName'].unique()] + [{'label': i, 'value': i} for i in df['name'].unique()],
        multi=True, placeholder='Filter by Name(FirstName or LastName)...'),
    html.Div(id='table-container')
    
    
])


@app.callback(dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])

def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    ## add an 'or' condition for the other column you want to use to slice the df 
    ## and update the columns that are displayeds
    #dff = df[df.name.str.contains('|'.join(dropdown_value)) ]
    #dff = df[df['name'].str.find('|'.join(dropdown_value)) != -1] 
    def get_ratio(row):
        name = row['name']
        return fuzz.token_sort_ratio(name, '|'.join(dropdown_value))
    
    dff = df[df.apply(get_ratio, axis=1) > 60]
    
    dff = dff[['name','title','citizenships','addresses','source_list_url','source_information_url']]
    return generate_table(dff)
# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, use_reloader=False)
