# NAME
#        clustering
#
# DESCRIPTION
#
#       The module 'clustering' contains methods for clustering on
#       nifti image collections extracted data
#
# AUTHORS
#
#       Raphaël AGATHON - Maxime CLUCHLAGUE - Graziella HUSSON - Valentina ZELAYA
#       Marie ADLER - Aurélien BENOIT - Thomas GRASSELLINI - Lucie MARTIN


from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.neighbors import DistanceMetric
from sklearn.metrics import silhouette_score, silhouette_samples, calinski_harabaz_score, euclidean_distances, \
    davies_bouldin_score
from sklearn.utils.extmath import row_norms, stable_cumsum
from scipy.spatial import distance
import numpy as np
import random
import math
import skfuzzy as fuzz

RANDMAX = 2**32 - 1

COLUMNS_INDEX = {
    'X': 0,
    'Y': 1,
    'Z': 2,
}


def format_ndarray(points, columns_selected) -> np.ndarray:
    columns_selected_index = [COLUMNS_INDEX[column] for column in columns_selected]
    return points[:, columns_selected_index]


def perform_kmeans(param_dict, points, columns_selected):
    points_formatted = format_ndarray(points, columns_selected)
    clustering = KMeans(n_clusters=int(param_dict["n_clusters"]), random_state=random.randint(0, RANDMAX),
                        init=param_dict["init"],
                        max_iter=int(param_dict["max_iter"])).fit(points_formatted)

    unique_labels, counts = np.unique(clustering.labels_, return_counts=True)
    label_counts = dict(zip(unique_labels, counts))

    # Reformat centers to be in 3D
    if len(columns_selected[0]) != 3:
        # Create a new centroids list
        centers = []
        for _ in range(param_dict["n_clusters"]):
            centers.append([0, 0, 0])
        # We addition all the coordinates in the centroids
        for point_index, label in enumerate(clustering.labels_):
            centers[label][0] = centers[label][0] + points[point_index][0]
            centers[label][1] = centers[label][1] + points[point_index][1]
            centers[label][2] = centers[label][2] + points[point_index][2]
        # We divide by the number of points in each label for each centroid to obtain the barycenter
        for i in label_counts.keys():
            centers[i][0] = centers[i][0] / label_counts[i]
            centers[i][1] = centers[i][1] / label_counts[i]
            centers[i][2] = centers[i][2] / label_counts[i]
    else:
        centers = clustering.cluster_centers_

    return {
        "labels": clustering.labels_,
        "centers": centers
    }


def perform_agglomerative_clustering(param_dict, points, columns_selected):
    points = format_ndarray(points, columns_selected)
    clustering = AgglomerativeClustering(n_clusters=int(param_dict["n_clusters"]), affinity=param_dict["affinity"],
                                         linkage=param_dict["linkage"]).fit(points)
    return {
        "labels": clustering.labels_,
        "hac": clustering,
    }


def perform_DBSCAN(param_dict, points, columns_selected):
    points = format_ndarray(points, columns_selected)
    dbscan = DBSCAN(eps=float(param_dict["eps"]), min_samples=int(param_dict["min_samples"]),
                    metric=param_dict["metric"]).fit(points)
    return {
        "labels": dbscan.labels_,
    }


def perform_kmedoids(param_dict, points, columns_selected):
    points_formatted = format_ndarray(points, columns_selected)
    distances_matrix_pairwise = compute_distances(points, param_dict['metric'])
    clustering_labels, clustering_medoids_index = kmedoids_cluster(str(param_dict["init"]), points_formatted,
                                                             distances_matrix_pairwise,
                                                             int(param_dict["n_clusters"]))

    # Reformat centers to be in 3D
    centers = []
    for index in clustering_medoids_index:
        centers.append(list(points[index, :3]))

    return {
        "labels": clustering_labels,
        "centers": centers,
    }


def perform_FuzzyCMeans(param_dict, points, columns_selected):
    points = format_ndarray(points, columns_selected)
    print("perform_FuzzyCMeans -> n_clusters : {}".format(int(param_dict["n_clusters"])))

    number_of_columns = len(columns_selected)

    # format the data the way fuzz need them to be
    to_stack = []
    for i in range(number_of_columns):
        to_stack.append(points[:, i])
    pts = np.vstack(to_stack)

    center, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(pts, int(param_dict["n_clusters"]), int(param_dict["m"]),
                                                       error=float(param_dict["error"]),
                                                       maxiter=int(param_dict["maxiter"]), seed=None)

    # Create a labels list for viewing purposes
    labels = []
    belong = []
    for col in range(len(u[0])):
        points_belonging = []
        line_max = 0
        belong_max = 0
        for line in range(len(u)):
            points_belonging.append(u[line][col])
            if u[line][col] > belong_max:
                belong_max = u[line][col]
                line_max = line
        labels.append(line_max)
        belong.append(points_belonging)

    return {
        "labels": labels,
        "belong": belong,
        "centers": center,
        "u": u,
        "fpc": fpc,
    }


# ------------------------------------- K Medoids implementation ------------------------------------------

def compute_distances(data_matrix, distance, normalize=False):
    """
    Compute distances between data points
    :param data_matrix: The array containing the data shape=(ND x 4)
    :param distance: 'euclidean' or 'manhattan'
    :param normalize: False by default
    :return: The symmetric matrix of distances
    """

    # Euclidean or Manhattan
    dist = DistanceMetric.get_metric(distance)
    # See sklearn.neighbors.DistanceMetric documentation to see the distance matrix returned
    return dist.pairwise(data_matrix)


def kmedoids_cluster(init_mode, data_matrix, distances, k=3):
    """
    Perform kmedoids clustering
    :param distances: The symmetric matrix of distances between data points
    :param k: number of clusters
    :return: array of cluster labels and latest medoids
    """

    # Pick k random medoids and keep their indexes in data_matrix
    curr_medoids_index = init_clusters(init_mode, data_matrix, k)

    curr_medoids = np.zeros(shape=(k, data_matrix.shape[1]))

    c = 0
    for index in curr_medoids_index:
        curr_medoids[c] = np.array(data_matrix[index])
        c = c + 1

    print("First curr_medoids_index", curr_medoids_index)

    old_medoids_index = np.array([-1] * k)
    new_medoids_index = np.array([-1] * k)

    while not (old_medoids_index == curr_medoids_index).all():

        # Assign each point to cluster with closest medoid.
        clusters = assign_points_to_clusters(curr_medoids_index, distances)

        # Update cluster medoids to be lowest cost point.
        for curr_medoid in curr_medoids_index:
            cluster = np.where(clusters == curr_medoid)[0]
            new_medoids_index[curr_medoids_index == curr_medoid] = compute_new_medoid(cluster, distances)

        c = 0
        for index in curr_medoids_index:
            curr_medoids[c] = np.array(data_matrix[index])
            c = c + 1

        old_medoids_index[:] = curr_medoids_index[:]
        curr_medoids_index[:] = new_medoids_index[:]

    clusters_labels = []
    c = 0
    for cluster_index in clusters:
        clust_i, = np.where(curr_medoids_index == cluster_index)
        clusters_labels.append(int(clust_i))
        c = c + 1

    # print("curr_medoids ->", curr_medoids)
    return clusters_labels, curr_medoids_index


def init_clusters(init_mode, data_matrix, k):
    centers_index = np.array([-1] * k)
    m = data_matrix.shape[0]  # number of points
    n = data_matrix.shape[1]  # number of features

    centers = np.empty((m, n), dtype=data_matrix.dtype)

    if init_mode == 'random':
        while not len(np.unique(centers_index)) == k:
            centers_index = np.array([random.randint(0, m - 1) for _ in range(k)])

    elif init_mode == 'k-means++':

        # precompute squared norms of data points
        x_squared_norms = row_norms(data_matrix, squared=True)

        # This is what Arthur/Vassilvitskii tried, in Arthur, D. and Vassilvitskii, S.
        # "k-means++: the advantages of careful seeding". ACM-SIAM symposium
        # on Discrete algorithms. 2007
        n_local_trials = 2 + int(np.log(k))

        # Pick first center randomly
        center_id = random.randint(0, m - 1)
        centers_index[0] = center_id
        centers[0] = data_matrix[center_id]

        # Initialize list of closest distances and calculate current potential
        closest_dist_sq = euclidean_distances(
            centers[0, np.newaxis], data_matrix, Y_norm_squared=x_squared_norms,
            squared=True)
        current_pot = closest_dist_sq.sum()

        # Pick the remaining n_clusters-1 points
        for c in range(1, k):
            # Choose center candidates by sampling with probability proportional
            # to the squared distance to the closest existing center
            rand_vals = np.random.random_sample(n_local_trials) * current_pot
            candidate_ids = np.searchsorted(stable_cumsum(closest_dist_sq),
                                            rand_vals)

            # Compute distances to center candidates
            distance_to_candidates = euclidean_distances(
                data_matrix[candidate_ids], data_matrix, Y_norm_squared=x_squared_norms, squared=True)

            # Decide which candidate is the best
            best_candidate = None
            best_pot = None
            best_dist_sq = None
            for trial in range(n_local_trials):
                # Compute potential when including center candidate
                new_dist_sq = np.minimum(closest_dist_sq,
                                         distance_to_candidates[trial])
                new_pot = new_dist_sq.sum()

                # Store result if it is the best local trial so far
                if (best_candidate is None) or (new_pot < best_pot):
                    best_candidate = candidate_ids[trial]
                    best_pot = new_pot
                    best_dist_sq = new_dist_sq

            centers_index[c] = best_candidate
            centers[c] = data_matrix[best_candidate]
            current_pot = best_pot
            closest_dist_sq = best_dist_sq

    else:
        raise ValueError('Init mode unknown !')

    return centers_index


def assign_points_to_clusters(medoids, distances):
    """
    Assign data entries to its nearest cluster based on distance to cluster's medoid
    :param medoids: An array containing the medoids of each cluster
    :param distances: The symmetric matrix of distances between data points
    :return:
    """
    distances_to_medoids = distances[:, medoids]
    clusters = medoids[np.argmin(distances_to_medoids, axis=1)]
    clusters[medoids] = medoids
    return clusters


def compute_new_medoid(cluster, distances):
    """
    Update the medoid point of each cluster after assigns
    :param cluster: The cluster of which the medoid should be updated
    :param distances: The symmetric matrix of distances between data points
    :return:
    """
    mask = np.ones(distances.shape)
    mask[np.ix_(cluster, cluster)] = 0.
    cluster_distances = np.ma.masked_array(data=distances, mask=mask, fill_value=10e9)
    costs = cluster_distances.sum(axis=1)
    return costs.argmin(axis=0, fill_value=10e9)


# --------------------------------------------------------------------------------------------------------


# -------------------------------- Clustering validation indexes ---------------------------------------
def compute_mean_silhouette(X, predicted_labels, metric='euclidean'):
    """
    Return the mean of samples' silhouette score on data according to assigned cluster labels
    :param X: The data matrix (n_samples x n_features)
    :param predicted_labels: the assigned cluster labels
    :param metric: metric used, euclidean distance by default
    :return: float between -1 and +1
    """
    X_filtered, predicted_labels = filter(X, predicted_labels)
    return silhouette_score(X_filtered, labels=predicted_labels, metric=metric)


def compute_samples_silhouette(X, predicted_labels, metric='euclidean'):
    """
    Return an array of size n_samples containing the silhouette scores for all data entries
    :param X: The data matrix (n_samples x n_features)
    :param predicted_labels: the assigned cluster labels
    :param metric: metric used, euclidean by default
    :return: an array (size n_samples) of floats between -1 and +1
    """
    X_filtered, predicted_labels = filter(X, predicted_labels)
    return silhouette_samples(X_filtered, labels=predicted_labels, metric=metric), predicted_labels


def compute_calinski_habaraz(X, predicted_labels):
    """
    Return the Calinski-Habaraz score for the predicted labels
    :param X: The data matrix : a list of n_features-dimensional data (each row corresponds to a single data point)
    :param predicted_labels:
    :return:
    """
    X_filtered, predicted_labels = filter(X, predicted_labels)
    return calinski_harabaz_score(X_filtered, labels=predicted_labels)


def compute_db(X, predicted_labels):
    """
    Compute the Davies-Bouldin score for a given clustering result
    :param X: The data matrix : a list of n_features-dimensional data (each row corresponds to a single data point)
    :param predicted_labels:
    :return:
    """

    X_filtered, predicted_labels = filter(X, predicted_labels)
    return davies_bouldin_score(X_filtered, labels=predicted_labels)


def compute_s(i, x, centroids, labels, cluster_number):
    norm = math.sqrt(cluster_number)
    s = 0
    for x in centroids:
        s += distance.euclidean(x, centroids[i])
    s = s / norm
    return s


def compute_Rij(i, j, x, centroids, labels, cluster_number):
    dist = distance.euclidean(centroids[i], centroids[j])
    Rij = (compute_s(i, x, centroids, labels, cluster_number) + compute_s(j, x, centroids, labels,
                                                                          cluster_number)) / dist
    return Rij


def compute_R(i, x, centroids, labels, cluster_number):
    list_R = []
    for i in range(cluster_number):
        for j in range(cluster_number):
            if i != j:
                Ri = compute_Rij(i, j, x, centroids, labels, cluster_number)
                list_R.append(Ri)
    return max(list_R)


def filter(X, predicted_labels):
    predicted_labels = list(predicted_labels)
    index_to_keep = [True if i != -1 else False for i in predicted_labels]
    for i in range(predicted_labels.count(-1)):
        predicted_labels.remove(-1)
    return X[index_to_keep], predicted_labels
