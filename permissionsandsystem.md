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
    /dev/nvme0n1p1 /mnt/nvme ext4 defaults 0 2

    

    /dev/nvme0n1p1: This is the device file for the NVMe partition you want to mount.
    /mnt/nvme: This is the mount point where the NVMe drive will be accessible in the filesystem.
    ext4: This is the filesystem type of the partition. It could be ext4, xfs, btrfs, etc., depending on what you formatted the drive with.
    defaults: This specifies the default mount options. It includes options like read/write access, automatic mounting, etc.
    0: This number indicates whether the filesystem should be dumped (backed up) using the dump command. A value of 0 means it will not be dumped.
    2: This number indicates the order in which filesystem checks (fsck) should be done at boot time. The root filesystem should have a value of 1, and other filesystems should have a value of 2. If you set it to 0, it will not be checked at boot.

