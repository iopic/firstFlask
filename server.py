from flask.templating import render_template
from forms import DocumentUploadForm
import os
from flask import current_app #for testing
from flask import Flask, flash, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import pandas as pd
import json
import plotly
from utils import pull_df, create_plot, prepare_chart

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'instance'), exist_ok=True)




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #print(dir(request))
    #print(request.form)
    #print(request.files)
    #print(request.method)
    #print(dir(request))
    #print(request.values)
    #print(request.form)
    form = DocumentUploadForm()
    #session['anyfile'] = False
    if session.get('filename') is None:
        full_filename = None
    else:
        full_filename = session.get('filename')
    #print(form)
    if form.validate_on_submit():
        #print(dir(form))
        #print(form.hidden_tag())
        #print(form.data)
        f = form.document.data
        res_path = form.result_path.data
        #print(dir(form.document))
        #print(form.document.has_file())
        filename = f.filename
        if res_path == "":
            save_path = app.instance_path
        else:
            save_path = res_path #will need to validate this...
        f.save(os.path.join(save_path,filename))
        flash("File successfull uploaded!","success")
        session['filename']= os.path.join(save_path,filename)
        #session.modified = True
        full_filename = session.get('filename')

        #get variable
       # v = form.to_graph.data
        #print(v)

    #get df
    df = pull_df(current_file=full_filename)

    #for testing
    feature = "Date" #need this until selector value possible
    #print(bar)
    chart_labels, chart_values,chart_type = prepare_chart(df,feature)
    

    return render_template('index.html', form=form,
            filename=full_filename,
            current_file = full_filename,
            labels = chart_labels,
            legend = 'hi',
            values = chart_values,
            headers = df.columns)



@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    print('hhhhhh')
    feature = request.args['selected']
    print(feature)
    graphJSON= create_plot(feature)

    return graphJSON

@app.route('/table_display', methods=['GET', 'POST'])
def table_display():
    df =  pd.read_csv(session['filename'])
    #df = df[['Status','Country']]
    # get table headers and rows
    columns = df.columns
    table_d = df.to_json(orient='index')
    rows = df.to_json(orient='values')


    return render_template('display.html', columns=columns, rows=json.dumps(rows))

if __name__ == "__main__":
  app.run(debug = True, port = 8000)