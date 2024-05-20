## Commands to run in cmd:

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Unix-like systems (Linux, macOS):
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt

# Set CrowdStrike API credentials (Windows)
set CROWDSTRIKE_CLIENT_ID=your_client_id_here
set CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here

# Set CrowdStrike API credentials (Unix-like systems)
# export CROWDSTRIKE_CLIENT_ID=your_client_id_here
# export CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here

# Run the connection test script
python test_crowdstrike_connection.py
