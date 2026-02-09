#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Streamlit app
# --server.port 8501: Default Streamlit port
# --server.address 0.0.0.0: Listen on all interfaces (required for VPS access)
# --server.headless true: Don't try to open a browser window on the server
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
