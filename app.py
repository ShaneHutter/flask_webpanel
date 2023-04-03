#!/usr/bin/env python3
"""Generic Flask Frontend (Public site) and Backend (Site panel)
"""

#from eventlet   import monkey_patch ; monkey_patch()

from fwp.config     import Config
from fwp.session    import gen_session_key

from flask          import (
    Flask, 
    redirect,   request,    render_template,
    url_for,    session,
    )

from flask_socketio             import SocketIO, emit
from flask_session              import Session
from flask_compress             import Compress
from flask_minify               import Minify
from flask_minify.decorators    import minify

from redis  import Redis

from werkzeug.middleware.proxy_fix import ProxyFix

# Load config
with Config( "app.yml" ) as conf:
    config = conf
app_name = config.get( "app.name" )


# Determine APP URLs
app_hostname = config.get( "app.hostname" )
app_ip = config.get( "app.ip" )
app_ports = config.get( "app.ports" )
app_protocols = config.get( "app.protocols" )
app_urls = [ 
    f"{protocol}://{host}:{port}" 
    for protocol , host , port in ( 
        ( protocol , host , port ) 
        for protocol in app_protocols 
        for host in [ app_hostname , app_ip ]
        for port in app_ports 
        ) 
    ]




# App setup
app_static_url_path = config.get( "app.static_url_path" )
app = Flask( __name__ , static_url_path = app_static_url_path )
app.wsgi_app = ProxyFix( app.wsgi_app , x_proto = 1 , x_host = 1 )

# Redis
redis_conf = config.get( "redis" )
redis_url = "redis://{host}:{port}".format( **redis_conf )
redis = Redis( **redis_conf )

# Session Setup
_session_key_name = f"{app_name}_session_key"
_secret_key = redis.get( _session_key_name )
if not _secret_key:
    _secret_key = gen_session_key()
    redis.set( _session_key_name , _secret_key )

# Minify
"""
    Use Minify decorator
    @minify( html = True , js = True , cssless = True )
"""
Minify( app , passive = True )

# Start Session
Session( app )

# Use Compression
if config.get( "app.use_compression" ):
    Compress( app )

# Setup SocketIO
_socketio = { 
    "async_mode": "eventlet",
    "manage_session": False,
    "message_queue": None, # Redis queue
    "cors_allowed_origins": app_urls,
    "engineio_logger": True,
    }
socketio = SocketIO( app , **_socketio )

@app.route( "/" )
@minify( html = True , js = True , cssless = True )
def index():
    data = {
        "title": app_name,
        "panel": True,      # This would be determined by a login session
        }
    return render_template( "index.jinja", data = data )