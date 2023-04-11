#!/usr/bin/env python3
"""fwp.config
"""

from .exceptions    import *

from yaml   import safe_load
from os     import getenv
from re     import split    as re_split
from locale import getdefaultlocale

class Config():
    def __init__( self , config_file ):
        self.config_file = config_file
        self.config = None
        self.extra_configs = {}
        self.defaults = {}
        self.language , self.encoding = getdefaultlocale()

    def __enter__( self ):
        self.load_config()
        return self

    def __exit__( self , *exception ):
        # Raise/Log for exception on exit
        return

    def load_config( self ):
        # Load main app config
        with open( self.config_file , "r" ) as config_file:
            self.config = safe_load(
                config_file.read()
                )
        # Set app_name
        self.app_name = self.config.get( "app" , {} ).get( "name" , "app_name" ).replace( " " , "_" )
        # Load extra configs defined in the main config
        _extra_configs = self.config.get( "extra_config" , {} )
        _extra_config_dir = _extra_configs.pop( "config_dir" , "" )
        if _extra_configs:
            self.config[ "extra" ] = {} 
            for name , filename in _extra_configs.items():
                with open( f"{_extra_config_dir}/{filename}" , "r" ) as config_file:
                    self.config[ "extra" ].update(
                        {
                            name: safe_load(
                                config_file.read()
                                )
                            }
                        )
        _locale = self.config.get( "locale" )
        if _locale:
            _lang = locale.get( "language" )
            if _lang:
                self.language = _lang
            _encode = locale.get( "encoding" )
            if _encode:
                self.encoding = _encode


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