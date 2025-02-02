# Reviving Old Hardware

Last week I installed Ubuntu on a recycled build:
 ```
Motherboard: Acer
Product Name: Nitro N50-600
CPU: Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz
GPU: Nvidia GeForce GTX 1050 Ti 4GiB GDDR5 
PSU: CX850M Corsair
S: Patriot NVMe 512gb
RAM: Crucial x2 8GiB @ 2400MT/s DDR4
``` 

Now you would think a graphics card from 2016 would be totally obsolete...
Or at least on Windows it was. 

Here are some commands for you to check all of this on linux:
```
MB: sudo dmidecode -t baseboard
CPU: lspcu
GPU: lspci | grep VGA
RAM: sudo dmidecode -t memory
STORAGE: lsblk -d -o NAME,TYPE,VENDOR,MODEL,SIZE
```

Make sure to have installed all the drivers needed, you can find them in the other guides in this repo. 
I will not go over steam either as there is a little to do (you can also find it in the main repo at the very end. And more info in commonissues) 

--- 

**Now let's work our way up.**

### Minecraft
We'll start with minecraft and finish with much larger game. Sorry in advance about the pictures.

Step 0: Prereqs
Nvidia drivers, X11 tools etc

I will also be testing with most setting on low, as I personally prefer performance over quality. 

I always start with minecraft for two reasons:

One they have the neat F3 with FPS, GPU, CPU etc 
Two it's a chunk based game so you it's a good baseline to compare. 

![20250202_133212](https://github.com/user-attachments/assets/549e6e1f-5b60-4b85-ab3c-c7c7bb78198b)
_Here we can tell it's using the right GPU_

![20250202_133223](https://github.com/user-attachments/assets/d912af97-7000-479d-a2f9-c28584df0d9c)

A whooping 400 fps (min 230 in loading).

### Rocket League

**SteamOS and Mac Beta Versions**
As we continue to upgrade Rocket League® with new technologies like DirectX 11 and a 64-bit client, it is no longer viable for us to maintain support for the macOS and Linux (SteamOS) platforms. As a result, the final patch for the macOS and Linux versions of Rocket League was released on March 10, 2020. This update disabled online functionality (such as Casual and Competitive Playlists) for players on macOS and Linux, but offline features including Local Matches, and splitscreen play are still accessible.

From the official store page you get this infoirmation. Yet the when checking proton compatibility https://www.protondb.com/ it pretty much says it's almost native using Proton. 

Which is a bit weird to me, becuse it just is behind a few clicks, downloads and toggles. 
Also have to log-in Epic Games, from steam app? xd

#### Stuck Processing Vulkan Shaders

![image](https://github.com/user-attachments/assets/6cb363b0-c389-4908-8be2-955fe6ca9af0)

![video tutorial](https://www.youtube.com/watch?v=IbIlBv9Yejo)

Now again I put all the settings on super low, performance, as I just want to play in smooth experience rather than looks. 
Also weird keeps validating or downloading, while the app is actually opened and I'm able to play. Or I have to start another download to open another app? 
Anyways... 


![20250202_141639](https://github.com/user-attachments/assets/aa75383d-55ed-45b2-b2e7-835c99a42818)


