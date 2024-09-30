#!/bin/bash

# Infinite loop to run the Python scripts every minute
while true; do

    # echo "Invoked at $(date +"%H:%M:%S.%3N")"
    
    # Execute the Python scripts
    python generate-swiss-clock.py
    python generate-date-image.py
    
    # Get the current epoch time with fractional seconds
    current_time=$(date +%s.%N)
    
    # Calculate the epoch time for the next minute
    # Extract the integer part of the current time
    current_epoch=$(echo "$current_time" | cut -d. -f1)
    # Compute the next minute's epoch time
    next_minute_epoch=$(( (current_epoch / 60 + 1) * 60 ))

    # Calculate the exact sleep duration needed
    # Adding a small delta (e.g., 0.5 seconds) to ensure the transition has occurred
    # 0.1 secs works on mac, adding a bit more to ensure buffer on lower powered Synology 
    sleep_duration=$(echo "$next_minute_epoch - $current_time + 0.5" | bc -l)

    # Sleep until just after the next minute starts
    # echo "Sleeping $sleep_duration"
    sleep "$sleep_duration"
done
