from flask.templating import render_template
from forms import DocumentUploadForm, Inputs
import os
from flask import Flask, flash, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import plotly.express as px
import pandas as pd
import json
import plotly
from utils import make_data, make_table, make_plotly

#UPLOAD_FOLDER = '/path/to/the/uploads'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'instance'), exist_ok=True)

CURRENT_FILE= None
column_names = ['Status','Country','count']


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global CURRENT_FILE
    form = DocumentUploadForm()
    variable = Inputs()
    #session['anyfile'] = False
    if session.get('filename') is None:
        full_filename = None
    else:
        full_filename = session.get('filename')
    #print(form)
    if form.validate_on_submit():
        f = form.document.data
        filename = f.filename
        f.save(os.path.join(app.instance_path,filename))
        flash("File successfull uploaded!","success")
        session['filename']= os.path.join(app.instance_path,filename)
        #session.modified = True
        full_filename = session.get('filename')
        #CURRENT_FILE = os.path.join(app.instance_path,filename)
    
    print(variable.myChoices)

    #prepare data
    df = make_data(current_file=full_filename)

    #for bar chart
    plot_json=make_plotly(df_grouped=df)

    #for table
    headers,values = make_table(df_grouped=df)
    print(full_filename)
    return render_template('index.html', form=form,
    variable = variable,
            filename=full_filename,
            plot_json=plot_json,
            current_file = full_filename,
            headers= headers, values = values)




@app.route("/plotly")
def plot_chartjs():
    # total confirmed cases globally
    print(session.get('filename'))
    if session.get('filename') is None:
        full_filename = None
    else:   
        full_filename = session.get('filename')
    df = make_data(current_file=full_filename)
    plot_json=make_plotly(df_grouped=df)
    #plot_json=make_data(current_file=session.get('filename'))

    return render_template('plotly_chart.html', plot_json = plot_json)


@app.route('/table')
def index():
    global CURRENT_FILE
    return render_template('ajax_table.html', title='Ajax Table',filename=CURRENT_FILE)


@app.route('/api/data')
def data():
    global CURRENT_FILE
    global column_names
    if CURRENT_FILE is None:
        df_grouped = pd.DataFrame(columns=column_names)
    else:
        data = pd.read_csv(CURRENT_FILE)
        #countries = ['Chile','South Africa']
        countries = ['Chile']
        df = data[data['Country'].isin(countries)]
        df_grouped = df.groupby(['Country','Status']).size().reset_index(name='count')

    return {'data': df_grouped.to_dict()}


if __name__ == "__main__":
  app.run(debug = True, port = 8000)