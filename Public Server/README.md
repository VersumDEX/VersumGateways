**Deployment:**

1. Set up MySQL Database for every currency (Litecoin, Bitcoin, Ethereum), with following tables:
	-unused_vaddresses (contains only fresh vaddresses)
	-unused_raddresses (cointains only fresh raddresses)
	-withdraw (contains both r- and vaddresses)
	-deposit (contains both r- and vaddresses)


2. Start a multichain node and give it admin rights

3. Edit config.py with the neccessary information

4. Install gunicorn to run server later

5. Configure Nginx as reverse proxy 

6. Start wsgi.py with gunicorn