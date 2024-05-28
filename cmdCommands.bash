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

# Run the connection test script
python APIconnectionTest.py

# Run the containment test simulation (without API)
python NoAPIsim.py

# Run the actual crowdstrike containment script
python ContainmentStatus.py

# Run the status update for contained hosts
python ContainmentStatus.py
