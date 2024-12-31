The installs themselves are pretty straight forward depending on distro:
The only things to be careful about: Where are you installing your OS and make sure your keyboard input layout is correct?
And set a root user & password! 

Make sure to use GPT partition as it's more modern and can support drives larger than 2TB. Unless specifically needed for the OS you are installing. 

You can use Rufus or Etcher for quick USBs!

## After initial install

```sudo apt update && sudo apt upgrade -y```

> **_NOTE:_**  While there might be many distros a lot of the kernel uses are similar so I'll try to not be too specific. 
> What is generic is to check your device for what components they have: Especially Graphics devices which often can cause issues. 
> The above can take a few minutes giving you time to do some Google work.

```lspci -nnk ``` 
To see all devices being detected including network, other devices, etc

```lspci | grep -i vga```
For GPU specifically

You can also use ```lscpu```

But if you're there already you probably understand CPU architectures :D
If you're unsure again best is to go down some Googling: From you computer's manufacturer website, then check CPU "architecture" or "instruction set"
64 bit, 32 bit, or ARM (Raspberri pi for example) 

This can get confusing because it is sometimes named AMD64 (86x64) because it was created by AMD, but doesn't mean it's not compatible with Intel. 
This is also the most adopted now, so most modern hardware will run this.

The same can be done with ```lsusb``` if you're using weird connectors. 

```sudo reboot``` after the update and upgrade are done. 

## When first upgrade is done

Now we can take care of graphics: 
For intel it is most of time already integrated... As it's a often used in "dual" graphics 

Then Nvidia:
```sudo apt install {nvidia-driver-XXX}```

For AMD it's a bit more fun: They are included in the Linux kernel due to their open-source. 
But you will need some tools for modern applications:

```sudo apt install mesa-vulkan-drivers mesa-utils``` 

> **_NOTE:_** It's best to go find on the official sites for compatibility:
> Device manufacturer (This gives you the full specs)
> Graphics provider (Specific version compatible with^^)

You will need to reboot again, then ```nvidia-smi``` to check or the mesa/vulkan equivalent.

## Keeping an install clean

Keep only essential packages, this both helps your system and makes you less vulnerable:

List all packages: It might seem like there is a lot of fluff depending on distro but if you're on a fresh install it's quite normal as it's all the system components.
This number is still 2-3x lower than a Windows counterpart.

```dpkg -l```

Check an individual problematic package: 

```dpkg -l | grep {package_name}```

Useful to check past pkg installs

```grep "install " /var/log/dpkg.log | tail```

## Update warnings ⚠️
These can happen quite frequently when one of the software providers you use didn't update to latest signatures. 
This will give you annoying errors

Here is how to fix it:

Removing
```sudo apt remove --purge {pkgs1} {pkgs2}```

To make sure dependencies are also removed
```sudo apt autoremove --purge```

----

Check the problematic package:

```grep -r "brave" /etc/apt/sources.list /etc/apt/sources.list.d/```

Remove it from sources list:

```sudo rm /etc/apt/sources.list.d/brave-browser-release.list```

Then run update to your packages lists again to remove the warning:
```sudo apt update```

If you 're still having issues with dependencies USE AT YOUR OWN RISK:

```sudo apt full-upgrade```

## Security 🔒

```sudo apt install ufw```
```sudo ufw enable```
```sudo ufw allow ssh``` Make sure to use keys :)

This will restrict incoming traffic, you can use a VPN for further anonimity. 

If you're running local servers: 
```sudo ufw allow 80/tcp``` 

To secure that further you can look into reverse proxies. 

## 🖥️ Remote desktop sessions

For some weird reason this can be quite annoying depending on the distro
> **_NOTE:_** One thing  I found to fix a lot of my issues is to create a second user with elevated privileges so that you can remote connect to it easily while keeping the device functional on it's own. 

```sudo apt install xrdp xserver-xorg-core```

```sudo systemctl enable xrdp```
```sudo systemctl start xrdp```

Check if it's running:

```sudo systemctl status xrdp```

```sudo adduser xrdp ssl-cert```

If not rebooting sometimes helps. 

----

If you have ufw enable make sure to ```sudo ufw allow 3389```
This is the standard port.

If you get a black screen you might need to ```echo "gnome-session" > ~/.xsession```
Depending on your desktop type. 

```ip addr show```

Then add the specific port 3389

It should look something like: 192.x.x.x:3390 and you DO NOT NEED to specify a user just yet.
Now this is where it usually fails because you're already in the session. To me the best is to make a second user for remote sessions:

```sudo adduser {rdpuser}```

Then give it privileges: ```sudo usermod -aG sudo {rdpuser}```

There you go :) You know how to make a good install. For cherry on the cake you can share a folder between all users (this could be your coding or media?)

```chmod 777 {/home/mainuser/shared-folder}```

Then you can login into this new user you created without breaking everything!

## Screen tear 📺
If you cannot find a solution you can temporarly still get in the app: try disabling gpu acceleration for a specific program when launching it through the Terminal: 
```{code} --disable-gpu```


## Packages
Flatpack is the most practical way to download apps in my opinion: They will be slightly heavier than on Windows because:
Many modern apps (like Stremio) are built using Electron, which bundles a full Chromium engine and Node.js runtime. This increases the size of the app significantly.

.deb packages will also work! dpkg is designed to work with these files. 
They will be lighter because they interact directly with the host system. 

But they install seemlessly with dependencies: 

```flatpak list
flatpak install 
flatpak uninstall 
flatpak uninstall --unused
flatpak remove --unused
```

Some distros like Linux Mint have a neat little software manager pre-installed!
Basically just uses Flatpack for people who don't like terminal. 

## Developer tools

I personally just get vs code from the official source and is nicely integrated with Python with the public Microsoft extensions.
The beauty of it is that a large part of linux itself uses python compatible libraries as it's all open-source. 


You can simply create a file called hello.py and click the python version at the bottom right to start creating a .venv

Then save your code and make sure to run it with the venv path to not get mixed with system wide packages:

```cd .venv```
```sudo ./bin/python3 hello.py ```


If you are going to work with PyQt6 and creating GUI you might need some tools:

```
sudo apt install -y libxcb1 libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libxcb-render0 libxcb-render-util0

(optional) sudo apt install -y qt6-base-dev qt6-wayland libqt5x11extras5
```


## Picking a distro

This part is obviously the all time neckbeard debate... But i will just go over the package managers:

Fedora-Based Distros (e.g., Fedora, CentOS Stream, AlmaLinux):
Package Manager: DNF (or YUM in older versions)

Arch-Based Distros (e.g., Arch Linux, Manjaro, EndeavourOS):
Package Manager: Pacman

Debian-Based Distros (e.g., Ubuntu, Linux Mint, Raspberry Pi OS):
Package Manager: APT (Advanced Package Tool)

## System Monitoring 📈

Many know ```htop``` which is great already but there is a special one to my heart because it looks cooler: 

``` sudo apt install btm ```
You can then simply launch it in terminal: ```btm```

## Making your desktop your own ! 

Linux is highly customizable in general. 

If you are using default Ubuntu GNOME desktop here is a hot tip:
I hate the fact you have to click 2 times to get to your apps...

```sudo apt install gnome-shell-extensions gnome-shell-extension-manager```

Then toggle ON: Ubuntu Dock

## Reviving Old Hardware @geerlingguy

From what I gather the older the hardware, the more lightweight the distro you will want to pick. 
This means either going the light Ubuntu distros (Mate or Xubuntu) route or Mint which is slightly lighter than Ubuntu.

But if it's not too old you can go for the regular long term support. 
You can also go XFCE route ( another lighter desktop), which might not look as polished but is lighter and has more performance on old hardware. 

## 📷 Working with cameras or HMDI inputs 🔌 

Again you might need some basic tools: 
```sudo apt install v4l-utils ffmpeg```

First check devices:
``` ls /dev/video* ```

----
Then check the ouput: 
```ffplay /dev/video0```
Or using VLC (open-source):
```vlc v4l2:///dev/video0```

----

Better yet use open-cv !
``` pip install opencv-python```

Then create a script:
```
import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, frame = cap.read()
    _, binary = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary', binary)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
```

You might need to give your user permissions run these seperatly: 
```
sudo usermod -a -G video $USER
newgrp video
```


### Working with USBs devices

As we mentionned above:

First find detected devices: ```lsusb```
Then we want to understand the devices endpoints IN/OUT: 

```lsusb -d {1c4f:007c} -v```

Now that we have the information we need we can try to interface with it, depending on device it might be really easy or the worst time of your life. 
----

``` pip install pyusb```

We'll create a simple keylogger for educational purposes but the idea can be replicated to other more intresting devices (say a fingerpint scanner!) 

```
import usb.core
import usb.util
import sys

VENDOR_ID = 0x1c4f ## You will find this using the command above
PRODUCT_ID = 0x007c # Same here

def inspect_device():
   device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
   if device is None:
       print("Keyboard not found")
       sys.exit(1)

   print(f"\nFound device: {hex(VENDOR_ID)}:{hex(PRODUCT_ID)}")
   
   for cfg in device:
       print(f"\nConfiguration {cfg.bConfigurationValue}:")
       for intf in cfg:
           print(f"\n\tInterface {intf.bInterfaceNumber}:")
           print(f"\tInterface class: {intf.bInterfaceClass}")
           
           for ep_num in range(intf.bNumEndpoints):
               ep = usb.util.find_descriptor(
                   intf,
                   custom_match=lambda e: \
                       usb.util.endpoint_address(e.bEndpointAddress) == ep_num + 1
               )
               if ep:
                   print(f"\n\t\tEndpoint {ep.bEndpointAddress:02x}h:")
                   print(f"\t\tDirection: {'IN' if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN else 'OUT'}")
                   print(f"\t\tAttributes: {ep.bmAttributes:02x}h")
                   print(f"\t\tMax packet size: {ep.wMaxPacketSize}")

   return device

def monitor_keyboard(device):
   if device.is_kernel_driver_active(0):
       device.detach_kernel_driver(0)
       print("Detached kernel driver")

   device.set_configuration()
   cfg = device.get_active_configuration()
   intf = cfg[(0,0)]
   
   ep = usb.util.find_descriptor(
       intf,
       custom_match=lambda e: \
           usb.util.endpoint_direction(e.bEndpointAddress) == \
           usb.util.ENDPOINT_IN
   )

   print("\nStarting keyboard monitor... Press Ctrl+C to exit")
   try:
       while True:
           try:
               data = ep.read(ep.wMaxPacketSize, timeout=1000)
               if data:
                   print(f"Raw data: {[hex(x) for x in data]}")
           except usb.core.USBError as e:
               if e.args[0] == 110:
                   continue
               else:
                   print(f"USB Error: {str(e)}")
                   break
   except KeyboardInterrupt:
       print("\nExiting...")
   finally:
       try:
           device.attach_kernel_driver(0)
           print("Reattached kernel driver")
       except:
           pass

if __name__ == "__main__":
   device = inspect_device()
   print("\nPress Enter to start monitoring keyboard...")
   input()
   monitor_keyboard(device)
```

Some devices need specific communications protocols: Say again this was a fingerprint scanner there would often be sent write data that 'activates' the fingerprint area then another to 'confirm'. 
You can often find the information online because some nerd reversed it or it's released by manufacturers. 







