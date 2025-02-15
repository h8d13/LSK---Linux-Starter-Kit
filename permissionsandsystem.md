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




Format and Mount NVMe Drive:

    You can use tools like gparted or command-line utilities to do this.
    Once formatted, you can mount the NVMe drive to a directory of your choice (e.g., /mnt/nvme).

Update fstab:

    If you want the NVMe drive to mount automatically at boot, you can add an entry to your /etc/fstab file.

