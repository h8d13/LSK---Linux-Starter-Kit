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

We'll start with minecraft and finish with much larger game. 

Step 0: Prereqs
Nvidia drivers, X11 tools etc

I will also be testing with most setting on low, as I personally prefer performance over quality. 

I always start with minecraft for two reasons:

One they have the neat F3 with FPS, GPU, CPU etc 
Two it's a chunk based game so you it's a good baseline to compare. 






