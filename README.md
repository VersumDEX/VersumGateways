**Versum Gateways - A Quick Overview**

The Gateway connects our blockchain with the world outside our ecosystem and allows our users to deposit & withdraw their funds to & from our blockchain.<br />
<br />
For a higher security level, our gateways consist of 2 different, spatially separated servers. <br />
All funds are stored on a hardened system and are represented in an immutable, decentralized way through the Versum Blockchain (Multichain Protokoll). The communication between the hardened Server & the User Client is done through a public server which sits between users & their funds, to shield the funds.<br />
<br />
The general concept of these gateways can (and will) be applied to other asset classes (like stocks or fiat money, etc.) with some modifications.<br />
<br />
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
	