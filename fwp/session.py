#/usr/bin/env python3
"""fwp.session"""

from os import urandom

def gen_session_key( length = 512 ):
    return urandom( length )