import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn import tree
from subprocess import check_call
import random as rd
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score


class CustomAHC(object):

    def __init__(self, filename, n_cluster=4):
        self.dataset_raw = pd.read_excel(filename)
        self.dataset = self.dataset_raw[["BookingMonth", "DestinationCity", "Product", "GrossWt", "VolumeWt"]]
        self.dataset.columns = ["M01", "M02", "M03", "M04", "M05"]
        self.serial_numbers = [x for x in self.dataset_raw["SNo"]]
        self.n_cluster = n_cluster
        self.X = None
        self.labels = list()
        self.count_labels = list()

    def transform(self):
        d = self.dataset.fillna(0)
        result = list()
        for i, row in d.iterrows():
            v1 = 0
            v2 = 0
            for x in range(1, 3):
                v1 += row[f"M0{x}"]
            for x in range(4, 6):
                v2 += row[f"M0{x}"]
            result.append([(v1 * (10 + rd.random()) / 2), (v2 * (10 + rd.random()) / 2)])
        self.X = pd.DataFrame(result).to_numpy()
        return pd.DataFrame(self.X)

    def get_cluster(self):
        model = AgglomerativeClustering(n_clusters=self.n_cluster, affinity='euclidean', linkage='single')
        model.fit(self.X)
        self.labels = model.labels_
        return model

    def get_result(self):
        list_df = list()
        list_cluster_label = list()
        self.dataset_raw["Label"] = self.labels
        count_label = list()
        for i in range(self.n_cluster):
            df = self.dataset_raw[self.dataset_raw["Label"] == i]
            list_df.append(df)
            list_cluster_label.append(f"Cluster {i}")
            count_label.append(len(df))
        self.count_labels = count_label
        return list_df, list_cluster_label
