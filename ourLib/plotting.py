# Imports for the plotting
import matplotlib.pyplot as plt
from nilearn import plotting, datasets
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np


def plot_3d_clusters(X : pd.DataFrame, y : list, title:str = "Result of the clustering" ):
    # Plot a figure
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.scatter3D(X['X'].values, X['Y'].values, X['Z'].values, c=y, cmap='Set1')
    # plt.show()
    color_dict = {0: 'red', 1: 'cyan', 2: 'magenta'}
    colors_list = []
    points_list = []
    for i in range(len(y)):
        points_list.append((X['X'][i], X['Y'][i], X['Z'][i]))
        colors_list.append(color_dict[y[i]])
    view = plotting.view_markers(points_list, colors_list, marker_size=10)
    view.open_in_browser()
    """
    color_dict = {0: 'red', 1: 'cyan', 2: 'magenta'}
    display = plotting.plot_anat()
    for i in range(len(y)):
        point = [(X['X'][i], X['Y'][i], X['Z'][i])]
        display.add_markers(point, marker_color=color_dict[y[i]])
    plotting.show()
    """