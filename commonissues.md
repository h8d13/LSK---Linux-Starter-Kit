# Common Issues

### Cannot locate packages (Ubuntu)

Fix: https://askubuntu.com/questions/378558/unable-to-locate-package-while-trying-to-install-packages-with-apt

----

### SESSION TYPE NOT SWITCHING 

  sudo echo $XDG_SESSION_TYPE

Want to try x11 from wayland?

Dont forget to 

sudo apt install xserver-xorg

Then restart and when logging back on kde small button to switch to x11.

Especially useful if you're on Windows user and want low level x11 access. See remote sessions in main readme file of this repo.

If you want to go a step further and develop directly with x11:

sudo apt install libx11-dev

You'll need to compile you can use gcc or make for convenience. Good luck!

sudo apt install build-essential
or 
sudo apt install cmake



----

### Graphics card not being used Linux

I've recently been installing Linux on older machines that have both an integrated GPU and a small NVIDIA card.

Here are the steps:
Make sure everything is up to date, check graphics drivers: ```nvidia-smi``` and ``` ubuntu-drivers devices``` this should detect your graphics card and recommend you the right version.

If not you need to find the right drivers follow install commands ```sudo apt install nvidia-driver-550```

Mine crashed during the end of the install but still worked? I guess just let it run even if it's not moving for a bit?

Then once you have that you you have to make sure you're in x11 and have both nvidia-prime and sudo apt install xserver-xorg-video-nouveau

Finally you can open NVIDIA X SERVER SETTINGS (just a fancy way of saying graphics libraries) 
![Screenshot_20250115_030005](https://github.com/user-attachments/assets/9c2cd7c9-2589-4828-a24a-76aebf7ac701)

Go to: PRIME Profiles and select NVIDIA Performance mode.

Now it will ask you to restart and voilà!

I also like to downlaod minecraft to check using F3 if it is actually using the GPU and usually you can see a x2 increase in FPS compared to integrated, even on older hardware. I got a nice stable 120 with a 950 with 2GB of memory. 


If you want to do that make sure you isntalled java ``` sudo apt install openjdk-17-jdk ```


![Screenshot_20250115_032303](https://github.com/user-attachments/assets/fabf93a1-a715-4e16-b530-2a73f3a34fea)



Last thing if you actually want to play a bit and your trackpad isn't working at the same time as your keys in KDE there is a switch for it in your settings directly:
![Screenshot_20250115_032505](https://github.com/user-attachments/assets/85582216-08d9-4d9d-bfde-b2be0c26d2c3)


---


### Veryfing Shim SBAT data failed: Security Policy Violation
Something has gone SERIOUSLY wrong with SBAT self-check failed: Security Policy Violation

FIX: (MSI motherboard) 

You have to find some boot setting in your BIOS:
Boot > Secure Boot
OS Type > Other OS

You might for some OSes also need to disable fast boot setting which can break installs. 
