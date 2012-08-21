#!/bin/bash
curl \
    -u shadowman:shadowman \
    -H 'Content-Type: application/json' \
    -X POST \
    --data @rhic.json \
    http://127.0.0.1:8000/api/rhic/  \
| python -mjson.tool
