## Find your sudoers file

/etc/sudoers
nano into it

Add the following line: 
`
<username> ALL=(ALL:ALL) ALL
`

Reload your terminal and you should be able to sudo. 

Find out more details about your system
---

cat /etc/os-release

Find the type of os and find the relative sources of Debian. 
/etc/apt/sources.list

Example for MacG5 powerPC:
```
deb http://deb.debian.org/debian/ buster main contrib non-free
deb http://deb.debian.org/debian/ buster-updates main contrib non-free
deb http://security.debian.org/debian-security buster-security main contrib non-free
```
