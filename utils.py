import pandas as pd
import plotly.express as px
import json
import plotly
from datetime import datetime
import plotly.graph_objs as go #for testing

import numpy as np


column_names = ['Status','Country','count']
#def get_data():
def make_table(df_grouped):
    """
    Return tuple of headers and data rows to populate table
    """
    if len(df_grouped) == 0:
        values = []
    else:
        values = []
        for row in df_grouped.to_dict(orient='records'):
            vals = []
            for k,v in row.items():
                vals.append(v)
            values.append(tuple(vals))
        

    return column_names, values

def pull_df(current_file):
    if current_file is None:
        df = pd.DataFrame(columns = ['Date','ISO','Country','Status','Note'])
    else:
        df = pd.read_csv(current_file)
        df['Date']=df['Date'].apply(lambda d: datetime.strptime(d, "%d/%m/%Y"))
    return df


def prepare_chart(df, feature):
    """
    feature = selected type from dropdown bar
    """
    if feature == "Date":
        chart_type = 'bar'
    else:
        chart_type = 'line'
    df_status = df.groupby(['Status']).size().reset_index(name='count')
    labels = df_status['Status'].tolist()
    values = df_status['count'].tolist()
    return labels,values, chart_type

### straight examples
def create_plot(feature):
    """
    feature = the value from the selector bar
    """
    if feature == 'Date':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'], # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON