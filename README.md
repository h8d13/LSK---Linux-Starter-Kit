# For Deb based systems 

The installs themselves are pretty straight forward depending on distro:
The only things to be careful about: Where are you installing your OS and make sure your keyboard input layout is correct? 

> **_NOTE:_** Use GPT for modern systems, especially if you need support for drives larger than 2TB or UEFI boot.
> However, if your system uses legacy BIOS, MBR may be required.
> For security reasons, many modern Debian-based systems disable the root account by default. I prefer to enable it, but you always have ```sudo``` for elevated tasks.

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

This can get confusing because it is sometimes named AMD64 (86x64) because it was created by AMD (then open-sourced, idk?), but doesn't mean it's not compatible with Intel. 
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
> You might need libdrm for older hardware

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

```grep -r {"brave"} /etc/apt/sources.list /etc/apt/sources.list.d/```

Remove it from sources list:

```sudo rm /etc/apt/sources.list.d/{brave-browser-release.list}```

Then run update to your packages lists again to remove the warning:
```sudo apt update```

If you 're still having issues with dependencies USE AT YOUR OWN RISK:

```sudo apt full-upgrade```

## Security 🔒


Check security updates are installed: 

```cat /etc/apt/apt.conf.d/20auto-upgrades```

Re-configure it ? 

``` sudo dpkg-reconfigure unattended-upgrades```

----

Firewall

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
> YOu could also just use VNC but that's cheating and increased latency with framebuffers :D

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

## Direct SSH access AND LOW LEVEL X11 ACCESS

One by one: 

``` sudo apt install openssh-server
sudo systemctl start ssh
sudo ufw allow ssh
sudo ufw allow 22
sudo systemctl status ssh
```
Regular SSH access: 

```ssh {user@host}```

Then from your Windows machine: Make sure you installed [ VC](https://vcxsrv.com/)
And launched it.

Check you are using X11 then follow:
```
echo $XDG_SESSION_TYPE
xhost +local:
export DISPLAY={windows_ip:0}
```

If the set up works it's incredibly cool, you can for example:

```
ssh -X user@linux_ip
firefox
```

It will look and feel like a normal window but is running on the linux system! 

![X11DIRECTACCESS](capcap.PNG)

It really isn't that complicated but the reason why these are set up like this is to prevent session hijacking: RSA host key fingerprint which is used to verify the server's identity in future connections to prevent man-in-the-middle attacks.
Why you should get a prompt at some point that generates the keys. 

This also means Native GPU/hardware access without added encoding/decoding. 
What I mean is xrdp is okay, X11 direct is incredible. Then VNC is the noob way. 

You can now chose between KDE, XFCE4 or whatver desktop you like... 
I like to keep the original user's desktop intact to always be able to control from there and install desktops on secondary users...


## Screen tear 📺 
Can happen sometimes if you made a mistake in drivers or your install was corrupted.
If you cannot find a solution you can temporarly still get in the app: try disabling gpu acceleration for a specific program when launching it through the Terminal: 
```{code} --disable-gpu```


<img src="weirdtear.webp" alt="screentearing" width="300">
(Windows example, but this happens sometimes when launching an app with GPU acceleration on debian systems, likely due to drivers)

If an issue like this persists; I would recommend checking if the installation was not corrupted somewhere along even at initial install..
Simple solution is to check compatibility issues and re-install a clean OS with more knowledge.

## Packages
.deb packages will also work! dpkg is designed to work with these files. 
They will be lighter because they interact directly with the host system. 

Flatpack is the most practical way to download apps in my opinion: They will be slightly heavier than on Windows because:
Many modern apps (like Stremio) are built using Electron, which bundles a full Chromium engine and Node.js runtime. This increases the size of the app significantly.

But they install seemlessly with dependencies: 

```flatpak install flathub com.stremio.Stremio```

Some distros like Linux Mint have a neat little software manager pre-installed!
Basically just uses Flatpack for people who don't like terminal. 

For Ubuntu, it will be snap packages by default. But you can easily install flatpack or deb packages too. 

Do be careful that .deb interacts with the host system so download from trusted sources. 

## Developer tools

I personally just get vs code from the official source and is nicely integrated with Python with the public Microsoft extensions.
The beauty of it is that a large part of linux itself uses python compatible libraries as it's all open-source. 


You can simply create a file called hello.py and click the python version at the bottom right to start creating a .venv

Then save your code and make sure to run it with the venv path to not get mixed with system wide packages:

```cd .venv```
```./bin/python3 hello.py ```


If you are going to work with PyQt6 and creating GUI you might need some tools:

```
sudo apt install -y libxcb1 libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libxcb-render0 libxcb-render-util0

(optional) sudo apt install -y qt6-base-dev qt6-wayland libqt5x11extras5
```

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

## 📷 Working with cameras or HMDI inputs 

Again you might need some basic tools: 
```sudo apt install vlc v4l-utils ffmpeg```

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


## Working with USBs devices 🔌 

As we mentionned above:

First find detected devices: ```lsusb```


Then we want to understand the devices endpoints IN/OUT, this will print all the verbose info:

```lsusb -d {1c4f:007c} -v```

#### Now that we have the information we need we can try to interface with it, depending on device it might be really easy or the worst time of your life. 

----

``` pip install pyusb```

We'll create a simple keylogger for educational purposes but the idea can be replicated to other more intresting devices (say a fingerpint scanner!) 

```
import usb.core
import usb.util

## QWERTY HEXADECIMAL VALUES
def get_key(data):
   keymap = {
       0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e', 0x09: 'f',
       0x0A: 'g', 0x0B: 'h', 0x0C: 'i', 0x0D: 'j', 0x0E: 'k', 0x0F: 'l',
       0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p', 0x14: 'q', 0x15: 'r',
       0x16: 's', 0x17: 't', 0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x',
       0x1C: 'y', 0x1D: 'z', 0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4',
       0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0'
   }
   return keymap.get(data[2], ''), hex(data[2]) if len(data) > 2 else ('', '')

## DETACH FROM KERNEL AND SPECIFY VENDOR+PRODUCT
def monitor_keyboard():
   device = usb.core.find(idVendor=0x1c4f, idProduct=0x007c)
   if device.is_kernel_driver_active(0):
       device.detach_kernel_driver(0)
   
   device.set_configuration()
   endpoint = device.get_active_configuration()[(0,0)][0]

   ### MAIN LOOP RETURN KEY, HEX AND DECIMAL VALUE
   try:
       while True:
           try:
               data = endpoint.read(8)
               key, hex_value = get_key(data)
               if key:
                   print(f"Key: {key} | Hex: {hex_value} | Decimal: {int(hex_value, 16)}")
           except usb.core.USBError as e:
               if e.args[0] != 110:
                   break
   except KeyboardInterrupt:
       device.attach_kernel_driver(0)

if __name__ == "__main__":
   monitor_keyboard()
```

Some devices need specific communications protocols: Say again this was a fingerprint scanner there would often be sent write data that 'activates' the fingerprint area then another to 'confirm'. 
You can often find the information online because some nerd reversed it or it's released by manufacturers. 


### BONUS 🎁

I've included some simple example scripts in the repo for general purposes and reference! 

![SYSTEMONITOR](capcapcap.PNG)

One of them is a green dot that is only green if:

cpu > 80%
ram > 85%
disk > 90%

It's simple but shows off PyQt integration with low level linux system using psutil. 

----

### One more bonus...
In a few clicks control other Linux systems (like a phone or tablet with Android) from you new system 😎

```sudo apt install adb scrcpy```

Connect it allow USB debugging (in settings developer mode) & file transfer
✅ Press always allow this computer

Check connection with adb devices
``` adb devices```
Then simply run: ```scrcpy``` 

Then you can interface with python this simply opens the clock app:

In your venv terminal:
```pip install pure-python-adb```

Then in python script:
```from ppadb.client import Client as AdbClient

# Connect to ADB
client = AdbClient(host="127.0.0.1", port=5037)
device = client.devices()[0]

# Launch the Samsung Clock app
device.shell("am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n com.sec.android.app.clockpackage/.ClockPackage")
```

You can now play Subway surfers on the side :D Or get neural network to play it for you hehe

``` 
from ppadb.client import Client as AdbClient

def swipe_screen(device, x1, y1, x2, y2, duration=2000):
    """
    Simulates a swipe gesture on the connected device.
    :param device: Connected ADB device.
    :param x1: Starting x-coordinate.
    :param y1: Starting y-coordinate.
    :param x2: Ending x-coordinate.
    :param y2: Ending y-coordinate.
    :param duration: ms
    """
    device.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
    print(f"Swiped from ({x1}, {y1}) to ({x2}, {y2}) over {duration}ms")

# Connect to ADB and device
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if not devices:
    print("No devices connected")
else:
    device = devices[0]
    print(f"Connected to device: {device.serial}")
    swipe_screen(device, 100, 1000, 100, 100, duration=1000)

```
----

You can go a step further to and install F-Droid and Termux on the tablet/phone itself to get a sub linux.

Go to: Settings > Briometrics and Security

Install unknown apps

Go to https://f-droid.org/en/ and download the apk
Then download termux
From F-Droid (Open-source)

Open termux 
Run ```pkg update```
```pkg upgrade```

You can then go full inception and download Python 
``` pkg install python ```

You could even run servers or a lightweight desktop on this hardware too. 
Altho mine is probably too old...

![ANDROID](capcapcapcap.PNG)


----

### FINAL BONUS AND I'M OUT:
 
After some googling I found out that the GNU project (Stands for GNU Not Unix) a lot of the commands you still use today, file system, bash, gcc, coreutils, POSIX standards, FHS is based/inspired by Unix.
An operating system that was dominant in entreprise in the 70-80s and that little hackers like yourself hated because they had to pay AT&T Bell Labs enourmous amounts for licenses. 
Minix was also another "copy" project made for students that was much cheaper alternative 'was about 70$ which you would get a book with :D

Peace <3


