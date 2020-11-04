import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("time_series_plotly.csv")
fig = px.scatter(df, x='Date', y='Case Count', color='County')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
markdown_text = '''
### Texas COVID-19 Dashboard
Creator: David O'Sullivan, [LinkedIn](www.linkedin.com/in/david-o-sullivan-ACE), [github](https://github.com/tower977)
This is my first interactive dashboard using Dash! Hope you like it!
This first plot is Texas COVID-19 accumulated cases by county over time
Source for data: [dshs.texas.gov](https://www.dshs.texas.gov/coronavirus/additionaldata/)
The next step is to create an interactive ashboard for Ireland and her counties.
'''
app.layout = html.Div([
    dcc.Markdown(children=markdown_text,
        style={
            'backgroundColor': colors['background'],
            'textAlign': 'center',
            'color': colors['text']
        }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
if __name__ == '__main__':
    app.run_server(debug=True)
