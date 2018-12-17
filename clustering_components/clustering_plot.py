"""
Here are made all the plotting functions
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from BrainMapper import compute_sample_silhouettes, get_current_usableDataset
import numpy as np
import pandas as pd
from nilearn import plotting


def plot_silhouette(labels, colors = None):
    # sampl
    # e_silhouettes = compute_sample_silhouettes(labels)
    sample_silhouettes = compute_sample_silhouettes(labels)
    average = np.mean(sample_silhouettes)

    # Dict of the form {label:[list of silhouettes]}
    labels_dict = {}

    for sample in zip(sample_silhouettes, labels):
        if sample[1] >= 0:
            labels_dict[sample[1]] = labels_dict[sample[1]] + [sample[0]] if sample[1] in labels_dict.keys() else [
                sample[0]]

    graph_offset = 1  # used to indicate the end of the last graph, so bar graphs don't overlap
    number_of_clusters = len(labels_dict.keys())
    colors = get_color(sorted(labels_dict.keys()))


    plt.figure()
    plt.xlim([np.min(sample_silhouettes), 1])
    plt.ylim([0,len(sample_silhouettes) + 1 + len(set(labels))]) # There is len(sample_silhouettes) and 1+len(set(labels)) blanks  
    for label in sorted(labels_dict.keys()):
        color=colors[label]
        y = sorted(labels_dict[label]+[np.min(labels_dict[label])]) # [np.min(labels_dict[label])] is here beacuse of step='pre' (we need 2 y to create a bar)
        plt.fill_betweenx(np.arange(graph_offset, graph_offset + len(y)),
                             0, y,
                             facecolor=color, edgecolor=color, alpha=0.7, step="pre")
        # plt.scatter(np.arange(graph_offset, graph_offset + len(y)),y, facecolor=color)
        plt.text(0.95, graph_offset + int(0.5 * len(y)), str(label), color=color)
        graph_offset += len(y)
    plt.title("The silhouette plot for the various clusters.")
    plt.xlabel("The silhouette coefficient values")
    plt.ylabel("Cluster label",labelpad=0.10)
    plt.yticks([])
    plt.show()


def plot_3d_clusters(labels: list, colors = None):
    # TODO mieux gérer les données en interne
    X = get_current_usableDataset().export_as_clusterizable()
    X = pd.DataFrame(X, columns=['X','Y','Z','Intensity'])

    color_dict = get_color(sorted(set(labels)))
    colors_list = []
    points_list = []
    for i in range(len(labels)):
        points_list.append((X['X'][i], X['Y'][i], X['Z'][i]))
        colors_list.append(color_dict[labels[i]])
    view = plotting.view_markers(points_list, colors_list, marker_size=10)
    view.open_in_browser()

def plot_cross_section(labels: list, colors = None):
    # TODO mieux gérer les données en interne
    X = get_current_usableDataset().export_as_clusterizable()
    X = pd.DataFrame(X, columns=['X','Y','Z','Intensity'])

    color_dict = get_color(sorted(set(labels)))
    display = plotting.plot_anat()
    for i in range(len(y)):
        point = [(X['X'][i], X['Y'][i], X['Z'][i])]
        display.add_markers(point, marker_color=color_dict[y[i]])
    plotting.show()

def get_color(distinct_labels: list) -> dict:
    """ Get a dict to homogeinize the colors
    
    Arguments:
        distinct_labels {list} -- [sorted list of the]
    
    Returns:
        dict -- [key = label: value = color]
    """

    number_of_clusters = len(distinct_labels)
    color_dict = {}
    for label in distinct_labels:
        color_dict[label] = cm.magma(float(label) / float(number_of_clusters))
    return color_dict

# if __name__ == "__main__":
#     from sklearn.datasets import make_blobs
#     from sklearn.cluster import KMeans
#     X,y = make_blobs(n_samples=100, n_f
# eatures=3, cluster_std=1.0, shuffle=True)
#     clustering = KMeans(n_clusters= 3).fit(X)
#     plot_silhouette(X, clustering.labels_)

