#!/bin/bash
curl -v -X PUT -H 'Content-Type: application/json' localhost:5000/measurements  -d @abbv7419.json
