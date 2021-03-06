import dash, plotly
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
from multipuller import puller

app = dash.Dash(__name__)

# app.css.append_css({ "external_url" : "https://codepen.io/chriddyp/pen/bWLwgP.css" })

app.layout = html.Div([
        html.Div(['Stock to plot: ',
                   dcc.Input(id='input', value='ACC', type='text'),
                 ],style = {'display':'inline-block'}),

        html.Div(['Time Interval: ',
                dcc.Dropdown(id='peri', options=[
                        {'label': '1', 'value': '61'},
                        {'label': '5', 'value': '301'},
                        {'label': '15', 'value': '901'}],value='61')
                ],style = {'display':'inline-block'}),
        dcc.Graph(id = 'livegraph_with_sma'),
        dcc.Graph(id = 'vol'),
        dcc.Graph(id = 'livegraph_with_bands'),
        dcc.Interval(id = 'interval_', interval = 60000)
])


@app.callback(
        Output('livegraph_with_sma', 'figure'),
        [Input(component_id = 'input', component_property = 'value'),
         Input(component_id = 'peri', component_property = 'value')],
        events=[Event('interval_', 'interval')]
        )
def update_graph(in_data, period):
    df = puller(STOCK=in_data, NO_OF_DAYS=1, EXCHANGE='NSE', INTERVAL=period, WRITE_TO_FILE = False)
    df['20MMA'] = df.Close.rolling(window=20).mean()
    df['30MMA'] = df.Close.rolling(window=30).mean()
    traces = []
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.Close,
            name = 'Close',
            mode = 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.20MMA,
            name = '20MMA',
            mode = 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.30MMA,
            name = '30MMA',
            mode = 'lines'))
            
    if period == '61':
        layout = plotly.graph_objs.Layout(title='1 Minute plot of '+in_data)
    elif period == '301':
        layout = plotly.graph_objs.Layout(title='5 Minute plot of '+in_data)
    else:
        layout = plotly.graph_objs.Layout(title='15 Minute plot of '+in_data)     
    return {'data': traces,'layout':layout}


@app.callback(
        Output('vol', 'figure'),
        [Input(component_id = 'stock_input', component_property = 'value'),
         Input(component_id = 'peri', component_property = 'value')],
        events=[Event('interval_', 'interval')]
        )
def update_graph_vol(in_data,period):
    df = puller(STOCK=in_data, NO_OF_DAYS=1, EXCHANGE='NSE', INTERVAL=period, WRITE_TO_FILE = False)
    traces = []
    
    traces.append(plotly.graph_objs.Bar(
            x = df.Time, y = df.Volume, name='Volume'))
    layout = plotly.graph_objs.Layout(title = 'Volume data for '+in_data)
    return {'data': traces,'layout':layout}


@app.callback(Output('livegraph_with_bands', 'figure'),
        [Input(component_id = 'input', component_property = 'value'),
         Input(component_id = 'peri', component_property = 'value')],
        events=[Event('interval_', 'interval')]
        )
def update_graph_bands(in_data,period):
    df = puller(STOCK=in_data, NO_OF_DAYS=1, EXCHANGE='NSE', INTERVAL=period, WRITE_TO_FILE = False)
    df['MMA20']=df.Close.rolling(window=20).mean()
    df['UpperBand']=df.MMA20 + (df.Close.rolling(window=20).std()*2)
    df['LowerBand']=df.MMA20 - (df.Close.rolling(window=20).std()*2)
        
    traces = []
    
    traces.append(plotly.graph_objs.Scatter(
            x=df.Time,y=df.Close,
            name='Close',
            mode= 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time, y = df.UpperBand,
            fill = None,
            line = dict(color='rgb(143, 19, 13)'),
            name = 'UB',
            mode = 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time, y = df.LowerBand,
            fill = 'tonexty',
            line = dict(color='rgb(143, 19, 13)'),
            name = 'LB',
            mode= 'lines'))

    layout = plotly.graph_objs.Layout(title = 'Bollinger Band for '+in_data)
        
    return {'data': traces,'layout':layout}

if __name__ == '__main__':
    app.run_server(debug=True)
