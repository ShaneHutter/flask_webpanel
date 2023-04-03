#!/usr/bin/env python3
"""fwp.config
"""

from .exceptions    import *

from yaml   import safe_load
from os     import getenv

class Config():
    def __init__( self , config_file = None ):
        self.config_file = config_file
        self.config = None

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

    def get( self , config_path ):
        """Get a config via it's path.

        order to look for config:
          - environment variable
          - config file
          - default
        """