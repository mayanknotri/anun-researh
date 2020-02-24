from flask import request, render_template
from webapp import app
from webapp.module.Research import CustomAHC
import os


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def load():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        global research
        file = request.files['file']
        n_cluster = int(request.form['n_cluster'])

        # Save file to tmp/
        file.save(os.path.join('webapp/tmp', 'dataset.xlsx'))

        research = CustomAHC(filename='webapp/tmp/dataset.xlsx', n_cluster=n_cluster)
        return render_template('view_data.html', tables=[research.dataset_raw.to_html(classes='table table-bordered',
                                                                                     index=False)])


@app.route('/transform', methods=['GET'])
def transform():
    global research
    df_transform = research.transform()
    return render_template('transform.html', tables=[research.dataset.to_html(classes='table table-bordered', index=False)])


@app.route('/result', methods=['GET'])
def result():
    global research
    research.get_cluster()

    list_df, list_cluster_label = research.get_result()
    return render_template('result.html', countLabels=research.count_labels, n=len(list_cluster_label),
                           list_df=list_df, list_cluster_label=list_cluster_label)
