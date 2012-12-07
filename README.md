A simple command-line to scrape Bandon FEWS (Flood Early Warning System) at http://www.bandonfloodwarning.ie/ into Google Fusion Tables and COSM/Pachube

Once per hour it grabs the river level data from the Bandon FEWS site and stores it in Google Fusion Tables and COSM

SETUP
1. You need to setup Google API Access at https://code.google.com/apis/console/ and create a project there to get keys
2. Rename client_secrets_sample.json to client_secrets.json and put those keys in client_secrets.json
3. sudo pip install google-api-python-client
4. First time you run it with --noauth_local_webserver to do the OAuth authentication which saves the credentials in plus.dat
5. From then on it's just:    python bandonfews3.py


2012/07/06
Moved to a public repo and included the code to push data to Cosm/Pachube

2012/12/07
Switched to new Google API Python Client and new Fusion Tables API. Much simpler/cleaner installation


