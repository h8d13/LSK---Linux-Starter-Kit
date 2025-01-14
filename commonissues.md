# Common Issues

### Veryfing Shim SBAT data failed: Security Policy Violation
Something has gone SERIOUSLY wrong with SBAT self-check failed: Security Policy Violation

FIX: (MSI motherboard) 

You have to find some boot setting in your BIOS:
Boot > Secure Boot
OS Type > Other OS

You might for some OSes also need to disable fast boot setting which can break installs. 

---

### Cannot locate packages (Ubuntu)

Fix: https://askubuntu.com/questions/378558/unable-to-locate-package-while-trying-to-install-packages-with-apt


### SESSION TYPE NOT SWITCHING 

Want to try x11 from wayland?

Dont forget to 

sudo apt install xserver-xorg

Then restart and when logging back on kde small button to switch to x11.

Especially useful if you're on Windows user and want low level x11 access. See remote sessions in main readme file of this repo.


