## Commands to run in cmd:

python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

-------------------------------------------------

pip install -r requirements.txt

--------------------------------------------------
set CROWDSTRIKE_CLIENT_ID=your_client_id_here
set CROWDSTRIKE_CLIENT_SECRET=your_client_secret_here
python test_crowdstrike_connection.py
