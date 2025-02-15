## Find your sudoers file

/etc/sudoers
nano into it

Add the following line: 
`
<username> ALL=(ALL:ALL) ALL
`

Reload your terminal and you should be able to sudo. 
