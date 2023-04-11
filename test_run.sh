#!/bin/bash
gunicorn -w1 -b 0.0.0.0:8080 app:app
