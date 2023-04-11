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
from os.path    import isdir , abspath , exists , basename
from yaml       import safe_load

def _lsdir_d( path ):
    """List directories in a path"""
    _ret = []
    for lsdir in glob( f'{path}/*' ):
        if isdir( lsdir ):
            _ret.append( 
                abspath( lsdir )
                )
    return _ret

def plugin_loader( plugin_dir ):
    """Load all plugins in the plugin_dir
    The plugin_dir contains direcories for each plugin.
    Each plugin will have a fwp-info.yml file that defines the plugin.

    This function will check for the plugin-info.yml file in the directory, then
    it will load the data from the yml file into a dictionary, and it will also
    save the plugin root directory into this data.
    """
    _ret = {}

    _dirs = _lsdir_d( plugin_dir )
    for _dir in _dirs:
        _plugin_info_file = f"{_dir}/plugin-info.yml"
        if exists( _plugin_info_file ):
            _basename = basename( _dir )
            with open( _plugin_info_file , "r" ) as plugin_info:
                _ret[ _basename ] = { "name": _basename }
                _ret[ _basename ].update(
                    safe_load(
                        plugin_info.read()
                        )
                    )
                if not _ret[ _basename ].get( "catagory" ):
                    _ret[ _basename ].update( { "catagory": _basename } )
                _ret[ _basename ].update( { "root_dir": _dir } )
    return _ret
