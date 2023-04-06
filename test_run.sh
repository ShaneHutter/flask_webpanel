#!/bin/bash
killall -9 gunicorn
gunicorn -w1 -b 0.0.0.0:8080 app:app
