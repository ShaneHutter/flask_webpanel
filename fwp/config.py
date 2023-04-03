#!/usr/bin/env python3
"""fwp.config
"""

from .exceptions    import *

from yaml   import safe_load
from os     import getenv
from re     import split    as re_split

class Config():
    def __init__( self , config_file = None ):
        self.config_file = config_file
        self.config = None
        self.defaults = {}

    def __enter__( self ):
        self.load_config()
        return self

    def __exit__( self , *exception ):
        # Raise/Log for exception on exit
        return

    def load_config( self ):
        if not self.config_file:
            raise NoConfigurationFile()
        with open( self.config_file , "r" ) as config_file:
            self.config = safe_load( config_file.read() )
            self.app_name = self.config.get( "app" , {} ).get( "name" , "" )

    def get( self , config_path ):
        """Get a config via it's path.

        order to look for config:
          - environment variable
          - config file
          - default
        """
        _path_split_regex = r"(?<!\\)\."
        _config_path = re_split( _path_split_regex , config_path )
        _env = getenv( f"{self.app_name}_{'_'.join(_config_path)}".upper() )

        def _get_via_path( data , conf_path , default = None ):
            _ret = data 
            for path in conf_path[ :-1 ]:
                _ret = _ret.get( path , {} )
            _ret = _ret.get( conf_path[ -1 ] , default )
            return _ret
        def _get_from_config( conf_path ):
            return _get_via_path( self.config , _config_path )
        def _get_from_default( conf_path ):
            return _get_via_path( self.defaults , _config_path )

        _config = _get_from_config( _config_path )
        _default = _get_from_default( _config_path )

        if _env:
            return _env
        elif _config:
            return _config
        elif _default:
            return _default
        else:
            return