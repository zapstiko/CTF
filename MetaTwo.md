# MetaTwo
**Nmap** : 
```
nmap -vvv -Pn --min-rate 3000 -p0-65535 --reason -T4
```
**wpscan** 
```
wpscan --rua -e ap,at,tt,cb,dbe,u,m -t 50 --url http://metapress.htb/ --plugins-detection aggressive --passwords /opt/seclists/Passwords/probable-v2-top1575.txt
```


