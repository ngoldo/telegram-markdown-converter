#!/bin/bash

# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required packages
pip3 install --upgrade pip
pip3 install --upgrade -r requirements-dev.txt
