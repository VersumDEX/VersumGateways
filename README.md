**Versum Gateways - A Quick Overview**

The Gateways consist of 2 Servers, to ensure maximum security of the users funds. 
All funds are stored on a hardened system (server2) and are represented in an immutable, decentralized way through the Versum Blockchain (Multichain Protokoll). 

The general concept of these gateways can (and will) be applied to other asset classes (like stocks or fiat money, etc.) with some modifications.

Public Server:<br />
-Running server.py & wsgi.py <br />
-Has Database to store connections between Versum- & real addresses (for deposits & withdraws)<br />
-Running Versum Blockchain Admin-Node to give new users send/receive permission<br />
-Nginx used as reverse proxy<br />
-private function are secured by password - this 	defenitely needs further improvement<br />
<br />
Hardened Server:<br />
-stores all users funds issued on Versums Blockchain<br />
-hardened Server<br />
-allows no incoming requests<br />
-runs all workers & Versum Admin-Node and a node for 	every supported currency<br />
-Requests address pairs from 1st server<br />
-Checks weather an amount has been sent to a gateway 	address and if so, issues the equivalent amount on the 	Versum Blockchain (on deposit) or on the native currency blockchain (on witrhdraw)<br />
-Refills public server with fresh addresses for deposit & withdraw<br />
	