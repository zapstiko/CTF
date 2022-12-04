# Namp
```sudo namp -sV -sC --min-rate 3000 -T4 $IP```
# SMB 
## SMB File Share Enumeration
```Command: smbclient -N -L \\\\$IP```
## connected SMB session
```
SMB:> mask ""
SMB:> recurse ON
SMB:> prompt OFF
SMB:> mget *
```

## DNS servers to confirm the system’s name
```Command: dig @IP +short support.htb any```
