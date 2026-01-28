#! /bin/bash

# Update the knowledge base

# Get the current date
current_date=$(date +%Y-%m-%d)

# Get the current time
current_time=$(date +%H:%M:%S)

# Get the current directory
current_directory=$(pwd)


cp -r ../SLR\ draft/ knowledge-base/
cp -r ../code/stego-side-wing/src/ ./knowledge-base/stego-side-wing