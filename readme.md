##P2P-DI system(Peer to peer with Distributed Index)

-A sophisticated P2P system implemented on Distributed index to share RFC Files between peers and whose functionality is controlled by a Registration Server.

## Description

-A registration server (RS), running on a well-known host and listening on a well-known port, keeps information about the active peers.
-When a peer decides to join the P2P-DI system, it opens a connection to the RS to register itself. 
-If this is the first time the peer registers with the P2P-DI system, it is given a cookie by the RS which identifies the peer. 
-The cookie is used by the peer in all subsequent communication with the RS.
-The peer closes this connection after registration. 
-When a peer decides to leave the P2P-DI system, it opens a new connection to the RS to inform it, and the RS marks the peer as inactive.
-Each peer maintains an RFC index with information about RFCs it has locally, as well as RFCs maintained by other peers it has recently contacted. 
-It also runs an RFC server that other peers may contact to download RFCs. 
-Finally, it also runs an RFC client that it uses to connect to the RS and the RFC server of remote peers.

## Modules used
-os
-platform
-shlex
-time
-re
-socket
-threading


## Usage

Step 1 : to run the server side

Run the Registration Server on the terminal using the following command: $python RS_ks.py (We have used python version 2.7)

Step 2 : to run the Peer side (RFC client and RFC server) (peer1_ks & peer2_ks)

[Scenario: peer1_ks and peer2_ks registers with RS_ks. peer2_ks downloads 2 RFC's from peer1_ks]

-Place the RFC's that needs to be downloaded by peer2_ks in the IP_Project\Client folder on the python current working directory where RS and peer1_ks are present.
-In the peer1_ks & peer2_ks declare the variable of your server IP address and Required RFC names [if any] as example mentioned below:
SERVER_NAME = '192.168.0.14'
RFC_Fetching_List = [8130,8131]
-Run the Registration server on some other machine.
-By Default we have added 2 rfc files in the peer1_ks code folder. So please have it in your working folder before you start the peer1_ks code.
-Open the terminal or python IDE and run the peer1_ks using the following command: $python peer1_ks.py
-Open the terminal or python IDE and run the peer2_ks using the following command: $python peer2_ks.py



Peer code # Sample output
Please refer peer2_ks_msg_format notes attached along with this folder.
RFC_index.txt, Timer.txt, cookie.txt files get generated at the IP_Project\Client folder of CWD.

RS code # Sample output
Please refer RS_ks_msg_format notes attached along with this folder.
Peer_Index.txt file gets generated at the IP_Project\server folder of CWD.


# Version
 - 1.0

#Authors
----
Kashish Singh, Sathwik Kalvakuntla

# License

  - All rights reserved by the owner and NC State University.
  - Usage of the code can be done post approval from the above.
