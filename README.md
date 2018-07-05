**Versum Gateways - A Quick Overview**

The Gateways consist of 2 Servers, to ensure maximum security of the users funds. 
All funds are stored on a hardened system (server2) and are represented in an immutable, decentralized way through the Versum Blockchain (Multichain Protokoll). 

The general concept of these gateways can (and will) be applied to other asset classes (like stocks or fiat money, etc.) with some modifications.

Public Server:
	-Running server.py & wsgi.py 
	-Has Database to store connections between Versum- & real 	addresses (for deposits & withdraws)
	-Running Versum Blockchain Admin-Node to give new users 	send/receive permission
	-Nginx used as reverse proxy
	-private function are secured by password - this 	defenitely needs further improvement

Hardened Server:
	-stores all users funds issued on Versums Blockchain
	-hardened Server
	-allows no incoming requests
	-runs all workers & Versum Admin-Node and a node for 	every supported currency
	-Requests address pairs from 1st server
	-Checks weather an amount has been sent to a gateway 	address and if so, issues the equivalent amount on the 	Versum Blockchain (on deposit) or on the native currency 	blockchain (on witrhdraw)
	-Refills public server with fresh addresses for deposit & 	withdraw
	