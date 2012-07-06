The Bandon FEWS scraper uses a few different scripts and libraries some of which had to be patched to get OAuth2 working correctly.

 sudo apt-get install subversion

Initial code was from:  svn checkout http://fusion-tables-client-python.googlecode.com/svn/trunk/ fusion-tables-client-python-read-only 

This was then patched from here:http://code.google.com/p/fusion-tables-client-python/issues/detail?id=4 which I had to do manually and tweak due to versioning issues and then clean up the sample code from oauth_example.py which was the basis of it.

I also had to install: sudo easy_install --upgrade google-api-python-client

I did a hard-coded hack of  /usr/local/lib/python2.6/dist-packages/google_api_python_client-1.0beta6-py2.6.egg/oauth2client/tools.py  to set  'auth_local_webserver', False

Obviously I setup a Project/App in the Google APIs Dashboard at https://code.google.com/apis/console/b/0/#project:1023347453927:access

That gave me the key and secret which is hardcoded in.

Data is then inserted (with checking for duplicates) into Google Fusion Tables here: https://www.google.com/fusiontables/DataSource?docid=103YIcARoxuaWT7NfZ8mVBzY554sF_3ONYC1N3DE

2012/07/06
Moved to a public repo and included the code to push data to Cosm/Pachube

The two Cron Jobs are:
05 * * * * /home/ubuntu/gitwork/bandonfews/bandonfews2.sh > /home/ubuntu/bandonfews.log
*/15 * * * * /home/ubuntu/gitwork/bandonfews/fews2cosm.sh > /home/ubuntu/fews2cosm.log

