import pandas as pd
import plotly.express as px
import json
import plotly


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


def make_data(current_file):
    global column_names
    print(current_file)
    if current_file =='None' or current_file is None:
        df_grouped = pd.DataFrame(columns=column_names)
    else:
        data = pd.read_csv(current_file)
        #countries = ['Chile','South Africa']
        countries = ['Chile','Belgium']
        df = data[data['Country'].isin(countries)]
        df_grouped = df.groupby(['Country','Status']).size().reset_index(name='count')
    return df_grouped

def make_plotly(df_grouped):
    fig = px.bar(df_grouped, x='Status',color = 'Country', y=['count'], title='Global daily new cases')
    #fig.update_xaxes(rangeslider_visible=False)
    #fig.show()
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    #labels = df_grouped['Status'].tolist()
    #values = df_grouped['count'].tolist()
    return  plot_json