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
        dcc.Graph(id='livegraph'),
        dcc.Interval(id='interval_',interval=60000)
])


@app.callback(
        Output('livegraph', 'figure'),
        [Input(component_id='input', component_property = 'value'),
         Input(component_id='peri', component_property = 'value')],
        events=[Event('interval_', 'interval')]
        )
def update_graph(in_data, period):
    df = puller(stock=in_data, no_of_days=1, Interval=period, write_to_file = False)
    df['MMA20'] = df.Close.rolling(window=20).mean()
    df['MMA30'] = df.Close.rolling(window=30).mean()
    traces = []
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.Close,
            name = 'Close',
            mode = 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.MMA20,
            name = 'MMA20',
            mode = 'lines'))
    traces.append(plotly.graph_objs.Scatter(
            x = df.Time,
            y = df.MMA30,
            name = 'MMA30',
            mode = 'lines'))
            
    if period == '61':
        layout = plotly.graph_objs.Layout(title='1 Minute plot of '+in_data)
    elif period == '301':
        layout = plotly.graph_objs.Layout(title='5 Minute plot of '+in_data)
    else:
        layout = plotly.graph_objs.Layout(title='15 Minute plot of '+in_data)
    return {'data': traces,'layout':layout}

if __name__ == '__main__':
    app.run_server(debug=True)
