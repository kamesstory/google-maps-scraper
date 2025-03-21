#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

echo "Setup complete! To start using the scraper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python google_maps_scraper.py" 