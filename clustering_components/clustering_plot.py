"""
Here are made all the plotting functions
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from BrainMapper import compute_sample_silhouettes, get_current_usableDataset
import numpy as np
import pandas as pd
from nilearn import plotting
import numpy as np
from scipy.cluster.hierarchy import dendrogram

def plot_silhouette(labels, colors = None):
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
    # Add the bars  
    for label in sorted(labels_dict.keys()):
        color=colors[label]
        y = sorted(labels_dict[label]+[np.min(labels_dict[label])]) # [np.min(labels_dict[label])] is here beacuse of step='pre' (we need 2 y to create a bar)
        plt.fill_betweenx(np.arange(graph_offset, graph_offset + len(y)),
                             0, y,
                             facecolor=color, edgecolor=color, alpha=0.7, step="pre")
        # plt.scatter(np.arange(graph_offset, graph_offset + len(y)),y, facecolor=color)
        plt.text(0.95, graph_offset + int(0.5 * len(y)), str(label), color=color)
        graph_offset += len(y)
    # Add the average silhouette
    plt.axvline(x=average, ymin=0, ymax=graph_offset, color='red', linestyle='--', label='average = {:.2f}'.format(average))

    plt.title("The silhouette plot for the various clusters.")
    plt.xlabel("The silhouette coefficient values")
    plt.legend()
    #plt.ylabel("Cluster label",labelpad=0.10)
    plt.yticks([])
    plt.show()


def plot_3d_clusters(labels: list, colors = None):
    points_list, colors_list = get_points_list_colors_list(labels)
    # TODO Tweak of mark_size ? For now 5 but we need to automatize the size choice
    view = plotting.view_markers(points_list, colors_list, marker_size=5)
    view.open_in_browser()

def plot_cross_section(labels: list, colors = None):
    # TODO choose the coordinates of the cut
    points_list, colors_list = get_points_list_colors_list(labels)
    display = plotting.plot_anat()
    for point,color in zip(points_list, colors_list):
        display.add_markers([point], marker_color=[color])
    plotting.show()

def plot_dendrogram(model):
    """ Plot a dendogram of a hierarchical agglomerative clustering
    
    Arguments:
        model -- result of an agglomerative clustering
    """

    # Children of hierarchical clustering
    children = model.children_
    labels=list(model.labels_)
    # print("plot_dendrogram --> children : ", children)

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    colors = get_color(set(labels), in_int=True)
    colors[-1] = (83, 135, 2)
    number_of_clusters = len(set(labels))

    for i in range(0,linkage_matrix.shape[0]-number_of_clusters+1):
        labels.append(labels[int(linkage_matrix[i][0])])
    for i in range(0,number_of_clusters-1):
        labels.append(-1)

    lis = []

    def link_color_func(k):
        color = colors[labels[k]]
        string = '#'
        lis.append(k)
        for c in color :
            cl = format(c, 'x')
            if len(cl)==1:
                cl = "0" + cl
            string = string + cl
        return string

    plt.figure()
    dendrogram(linkage_matrix, link_color_func=link_color_func)
    plt.title('Dendrogram')
    plt.ylabel('Distance')
    plt.show()

def get_points_list_colors_list(labels : list) -> (list, list):
    """ Obtains the points list and colors list from labels.
    It is used in the function that are based on nilearn plotting.
    
    Arguments:
        labels {list} -- labels resulting of a clustering
    
    Returns:
        points list, colors list
    """
    X = get_current_usableDataset().export_as_clusterizable()
    X = pd.DataFrame(X, columns=['X','Y','Z','Intensity'])

    color_dict = get_color(sorted(set(labels)))
    colors_list = []
    points_list = []
    for i in range(len(labels)):
        points_list.append([X['X'][i], X['Y'][i], X['Z'][i]])
        colors_list.append(color_dict[labels[i]])
    return points_list, colors_list

    


def get_color(distinct_labels: list, in_int: bool = False) -> dict:
    """ Get a dict to homogeinize the color
    
    Arguments:
        distinct_labels {list} -- [**sorted** list of the **distinct** labels]
        in_int {bool} -- set to True if you want rgba in int [0,255] else default to False and rgba in float [0,1]
    Returns:
        dict -- [key = label: value = color in rgba]
    """

    number_of_clusters = len(distinct_labels)
    color_dict = {}
    for label in distinct_labels:
        color_dict[label] = cm.magma(float(label) / float(number_of_clusters), bytes=in_int)
    return color_dict

# if __name__ == "__main__":
#     from sklearn.datasets import make_blobs
#     from sklearn.cluster import KMeans
#     X,y = make_blobs(n_samples=100, n_f
# eatures=3, cluster_std=1.0, shuffle=True)
#     clustering = KMeans(n_clusters= 3).fit(X)
#     plot_silhouette(X, clustering.labels_)

