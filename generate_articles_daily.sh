#!/bin/bash

# Script to generate daily articles

echo "Generating daily articles..."

# Activate virtual environment if it exists
if [ -f "mackney-gazette-venv/bin/activate" ]; then
    source mackney-gazette-venv/bin/activate
    echo "Activated virtual environment"
fi

# Run the article generation script
python -m src.generate_articles_daily "$@"

# Exit with the same status as the Python script
exit $?
