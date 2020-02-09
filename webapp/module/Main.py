from flask import request, render_template
from webapp import app
from webapp.module.Research import FuzzyCMeans
import os


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def load():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        global fuzzyCMeans
        file = request.files['file']
        n_cluster = int(request.form['n_cluster'])

        # Save file to tmp/
        file.save(os.path.join('webapp/tmp', 'dataset.xlsx'))

        fuzzyCMeans = FuzzyCMeans(filename='webapp/tmp/dataset.xlsx', n_cluster=n_cluster)
        return render_template('view_data.html', tables=[fuzzyCMeans.dataset.to_html(classes='table table-bordered',
                                                                                     index=False)])


@app.route('/transform', methods=['GET'])
def transform():
    global fuzzyCMeans
    df_transform = fuzzyCMeans.transform()
    return render_template('transform.html', tables=[df_transform.to_html(classes='table table-bordered', index=False)])


@app.route('/result', methods=['GET'])
def result():
    global fuzzyCMeans
    fuzzyCMeans.clustering()
    base64Image = str(fuzzyCMeans.get_image(), 'utf-8', 'ignore')
    return render_template('result.html', base64Image=base64Image)
