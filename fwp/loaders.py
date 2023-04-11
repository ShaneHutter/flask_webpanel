#!/usr/bin/env python3
"""fwp.loaders

Description:
    This module handles functions for loading various data sets into dictionaries.
    It is useful for loading:
        - plugins
        - consoles
        - themes
        - etc...

Code Author:
    Shane Hutter <shane@intentropy.au>
"""

from glob       import glob
from os.path    import isdir

def _lsdir( path ):
    """List directories in a path"""
    _ret = []
    for lsdir in glob( f'{path}/*' ):
        if isdir( lsdir ):
            _ret.append( lsdir )
    return _ret

def plugin_loader( plugin_dir ):
    """Load all plugins in the plugin_dir
    The plugin_dir contains direcories for each plugin.
    Each plugin will have a fwp-info.yml file that defines the plugin.

    This function will check for the fwp-info.yml file in the directory, then
    it will load the data from the yml file into a dictionary, and it will also
    save the plugin root directory into this data.
    """
