from __future__ import division, print_function
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import skfuzzy as fuzz
import base64

matplotlib.use("agg")


class FuzzyCMeans(object):

    def __init__(self, filename, n_cluster):
        self.dataset = pd.read_excel(filename)
        self.n_cluster = n_cluster
        self.data_transform = pd.DataFrame()
        self.base64Image = None
        self.fig = None

    def transform(self):
        df = self.dataset[['BookingMonth', 'DestinationCity', 'Product', 'GrossWt', 'VolumeWt']]
        df = df.dropna(axis=0, how='any')
        df.columns = ['BookingMonth', 'DestinationCity', 'Product', 'Gross', 'Volume']
        df.loc[df['Product'] == 'REGPACK', 'Product'] = 2
        df.loc[df['Product'] == 'ONEPACK', 'Product'] = 1
        self.data_transform = df
        return self.data_transform

    def clustering(self):
        colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

        # Generate test data
        np.random.seed(42)  # Set seed for reproducibility
        apts = np.zeros(1)
        bpts = np.zeros(1)
        cpts = np.zeros(1)
        dpts = np.zeros(1)
        epts = np.zeros(1)

        for i, x in self.data_transform.iterrows():
            apts = np.hstack((apts, np.random.standard_normal(100) * x['BookingMonth']))
            bpts = np.hstack((bpts, np.random.standard_normal(100) * x['DestinationCity']))
            cpts = np.hstack((cpts, np.random.standard_normal(100) * x['Product']))
            dpts = np.hstack((dpts, np.random.standard_normal(100) * x['Gross']))
            epts = np.hstack((epts, np.random.standard_normal(100) * x['Volume']))

        # Visualize the test data
        alldata = np.vstack((apts, bpts, cpts, dpts, epts))

        n_cluster = 4
        cntr, u_orig, u0, d, jm, p, fpc = fuzz.cluster.cmeans(data=alldata, c=n_cluster,
                                                              m=2, error=0.005, maxiter=100)

        # Show 3-cluster model
        fig2, ax2 = plt.subplots()
        ax2.set_title('Trained model')
        symbols = ['o', 'x', 's', 'x', 'x', 'd']
        for j in range(n_cluster):
            ax2.plot(alldata[0, u_orig.argmax(axis=0) == j],
                     alldata[1, u_orig.argmax(axis=0) == j], symbols[j],
                     label='Cluster ' + str(j))
        self.fig = fig2

    def get_image(self):
        fig_file = BytesIO()
        self.fig.savefig(fig_file, format='png')
        fig_file.seek(0)  # rewind to beginning of file
        self.base64Image = base64.b64encode(fig_file.getvalue())
        return self.base64Image
