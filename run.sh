#!/bin/sh

# Infinite loop to run the Python script every 60 seconds
while true; do
    python generate-swiss-clock.py
    python generate-date-image.py 
    sleep 15
done
