#!/bin/bash
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
fi

if command -v gunicorn &> /dev/null; then
    gunicorn app:app -b 127.0.0.1:5001
else
    python3 -m flask run -h 127.0.0.1 -p 5001
fi
