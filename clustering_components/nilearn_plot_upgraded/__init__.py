"""
Plotting code for nilearn
"""
# Original Authors: Chris Filo Gorgolewski, Gael Varoquaux

def _set_mpl_backend():
    try:
        # We are doing local imports here to avoid poluting our namespace
        import matplotlib
        import os
        import sys
        # Set the backend to a non-interactive one for unices without X
        if (os.name == 'posix' and 'DISPLAY' not in os.environ
            and not (sys.platform == 'darwin'
                     and matplotlib.get_backend() == 'MacOSX'
                     )):
            matplotlib.use('Agg')
    except ImportError:
        print('matplotlib not installed')
        raise
    else:
        from nilearn.version import (_import_module_with_version_check,
                               OPTIONAL_MATPLOTLIB_MIN_VERSION)
        # When matplotlib was successfully imported we need to check
        # that the version is greater that the minimum required one
        _import_module_with_version_check('matplotlib',
                                          OPTIONAL_MATPLOTLIB_MIN_VERSION)

_set_mpl_backend()

from .html_connectome import view_markers

__all__ = ['view_markers']
