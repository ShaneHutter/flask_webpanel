#!/usr/bin/env python3
"""Generic Flask Frontend (Public site) and Backend (Site panel)
"""

from eventlet   import monkey_patch ; monkey_patch()

from fwp            import PKG_INFO
from fwp.config     import Config
from fwp.session    import gen_session_key
from fwp.loaders    import plugin_loader

from flask          import (
    Flask, 
    redirect,   request,    render_template,
    url_for,    session,    abort,
    )

from flask_socketio             import SocketIO, emit
from flask_session              import Session
from flask_compress             import Compress
from flask_minify               import Minify
from flask_minify.decorators    import minify

from redis  import Redis

from yaml   import safe_load
from glob   import glob

from werkzeug.middleware.proxy_fix import ProxyFix

# Load config
_config_file = "etc/fwp/app.yml"
with Config( _config_file ) as conf:
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

# App_data, define elsewhere
app_data = {
    "title": app_name,
    "description": config.get( "app.description" ),
    "panel": config.get( "extra.panel" ),
    "load_js": config.get( "site.load_js" ),
    "left_menu": config.get( "left_menu" ),
    "pkg_info": PKG_INFO,
    "plugins": plugin_loader( "etc/fwp/plugins" ),
    }

@app.route( "/" )
#@minify( html = True , js = True , cssless = True )
def index():
    return render_template( "index.jinja", data = app_data )

@app.route( "/js/<string:js_file>.js" )
#@minify( html = True , js = True , cssless = True )
def handle_js( js_file ):
    # 404 if not available
    available_js = []
    for jinja_file in glob( "templates/js/*.jinja" ):
        available_js.append( jinja_file.split( "/" )[ -1 ].split( "." )[ 0 ] )
    if js_file not in available_js:
        # Try static before 404
        abort( 404 )
    style_data = config.get( "extra.style" )
    data = {
        "app_ata": app_data,
        "style": style_data,
        "js_file": js_file,
        }
    return render_template( "js_loader.jinja" , data = data )
