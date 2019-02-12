import json
import numpy as np
from scipy import sparse
from nilearn import datasets
from . import cm

from .js_plotting_utils import (add_js_lib, HTMLDocument, mesh_to_plotly,
                                encode, colorscale, get_html_template,
                                to_color_strings)

# symbols used for the nilearn plot
SYMBOLS = ["circle", "square", "diamond", "x"]  # "diamond-open","circle-open","square-open"


class ConnectomeView(HTMLDocument):
    pass


def _get_markers(coords, colors):
    connectome = {}
    coords = np.asarray(coords, dtype='<f4')
    x, y, z = coords.T
    for coord, cname in [(x, "x"), (y, "y"), (z, "z")]:
        connectome["_con_{}".format(cname)] = encode(
            np.asarray(coord, dtype='<f4'))
    connectome["marker_color"] = to_color_strings(colors)
    connectome["markers_only"] = True
    return connectome


def _add_centers(connectome, centers_coords, centers_colors):
    coords = np.asarray(centers_coords, dtype="<f4")
    x, y, z = coords.T
    for coord, cname in [(x, "x"), (y, "y"), (z, "z")]:
        connectome["_centers_con_{}".format(cname)] = encode(
            np.asarray(coord, dtype='<f4')
        )
    connectome["centers_colors"] = to_color_strings(centers_colors)
    connectome["centers_symbols"] = [SYMBOLS[i % 5] for i in range(len(centers_coords))]


def _add_noise(connectome, noise_coords, noise_colors):
    coords = np.asarray(noise_coords, dtype="<f4")
    x, y, z = coords.T
    for coord, cname in [(x, "x"), (y, "y"), (z, "z")]:
        connectome["_noise_con_{}".format(cname)] = encode(
            np.asarray(coord, dtype='<f4')
        )
    connectome["noise_colors"] = to_color_strings(noise_colors)
    connectome["noise_symbol"] = SYMBOLS[0]


def _make_connectome_html(connectome_info, embed_js=True):
    plot_info = {"connectome": connectome_info}
    mesh = datasets.fetch_surf_fsaverage()
    # Load https://www.nitrc.org/frs/download.php/10846/fsaverage.tar.gz files pial left and pial right
    # To plot in 3D
    for hemi in ['pial_left', 'pial_right']:
        plot_info[hemi] = mesh_to_plotly(mesh[hemi])
    as_json = json.dumps(plot_info)
    as_html = get_html_template('connectome_plot_template.html').replace(
        'INSERT_CONNECTOME_JSON_HERE', as_json)
    as_html = add_js_lib(as_html, embed_js=embed_js)
    return ConnectomeView(as_html)


def view_markers(coords, colors, labels, marker_size=5., centers=None, centers_colors=None):
    """
    Insert a 3d plot of markers in a brain into an HTML page.

    Parameters
    ----------
    coords : ndarray, shape=(n_nodes, 3)
        the coordinates of the nodes in MNI space.

    colors : ndarray, shape=(n_nodes,)
        colors of the markers: list of strings, hex rgb or rgba strings, rgb
        triplets, or rgba triplets (i.e. formats accepted by matplotlib, see
        https://matplotlib.org/users/colors.html#specifying-colors)

    marker_size : float, optional (default=3.)
        Size of the markers showing the seeds.

    Returns
    -------
    ConnectomeView : plot of the markers.
        It can be saved as an html page or rendered (transparently) by the
        Jupyter notebook. Useful methods are :

        - 'resize' to resize the plot displayed in a Jupyter notebook
        - 'save_as_html' to save the plot to a file
        - 'open_in_browser' to save the plot and open it in a web browser.

    See Also
    --------
    nilearn.plotting.plot_connectome:
        projected views of a connectome in a glass brain.

    nilearn.plotting.view_connectome:
        interactive plot of a connectome.

    nilearn.plotting.view_surf, nilearn.plotting.view_img_on_surf:
        interactive view of statistical maps or surface atlases on the cortical
        surface.

    """

    noise_coords = None
    noise_colors = None

    if colors is None:
        colors = ['black' for i in range(len(coords))]

    if -1 in labels:
        # If we have the result of DBSCAN
        # We need to filter the noise
        # We put information about noise points in noise_coords and noise_colors
        # we put information about not noise points in points_coords, points_colors and points_labels
        # At the end of the forloop, we rewrite coords, colors and labels with the not noise information
        points_coords = []
        points_colors = []
        points_labels = []
        noise_coords = []
        noise_colors = []
        for label, coord, color in zip(labels, coords, colors):
            if label == -1:
                noise_coords.append(coord)
                noise_colors.append(color)
            else:
                points_coords.append(coord)
                points_colors.append(color)
                points_labels.append(label)
        coords = points_coords
        colors = points_colors
        labels = points_labels

    # We choose the symbol from the label associated with the point
    # connectome_info is a dictionnary that will be passed as JSON to html view
    # It contains all the necessary information
    connectome_info = _get_markers(coords, colors)
    connectome_info["symbol"] = [SYMBOLS[i % 5] for i in labels]

    if centers is not None:
        # If we have centers , we add the data
        _add_centers(connectome_info, centers, centers_colors)

    if noise_coords is not None:
        # If we have noise , we add the data
        _add_noise(connectome_info, noise_coords, noise_colors)

    connectome_info["marker_size"] = marker_size
    connectome_info["center_size"] = 2 * marker_size
    connectome_info["noise_size"] = int(0.8 * marker_size)

    return _make_connectome_html(connectome_info)
