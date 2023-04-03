#!/usr/bin/env python3
"""Generic Flask Frontend (Public site) and Backend (Site panel)
"""

from eventlet   import monkey_patch ; monkey_patch()

from flask          import (
    Flask, 
    redirect,   request,    render_template,
    url_for,    session,
    )

from flask_socketio import SocketIO, emit
from flask_session  import Session
from flask_compress import Compress

from werkzeug.middleware.proxy_fix import ProxyFix

# Load site config - {{ app_name }}.yaml
app_hostname = "localhost"
app_ip = "127.0.0.1"
app_ports = [ "8080" ]
app_protocols = [ "http" , "https" ]
app_urls = [ 
    f"{protocol}://{host}:{port}" 
    for protocol , host , port in ( 
        ( protocol , host , port ) 
        for protocol in protocols 
        for host in [ app_hostname , app_ip ]
        for port in app_ports 
        ) 
    ]
app_use_compression = True
app_static_url_path = ""

redis_host = {
    "host": "127.0.0.1",
    "port": 6379,
    }
redis_url = "redis://{host}:{port}".format( **redis_host )



# App setup
app = Flask( __name__ , static_url_path = app_static_url_path )
app.wsgi_app = ProxyFix( app.wsgi_app , x_proto = 1 , x_host = 1 )


# Session Setup

# Start Session

# Use Compression

# Setup SocketIO
_socketio = { 
    "async_mode": "eventlet",
    "manage_session": False,
    "message_queue": None, # Redis queue
    "cors_allowed_origins": app_urls,
    "engineio_logger": True,
    }
socketio = SocketIO( app , **_socketio )
