# Image processing techniques

This is what got me into python more and more realizing that a video, is just a set of images. And images can be broken down quite easily. 

The idea is that you also get a visual output instantly which just makes it fun. 

There are also some intresting maths you can do. 

Simple example is clipping highest/lowest percentiles. 

![image](https://github.com/user-attachments/assets/bfc1cdfd-5814-4ee3-8f64-42e119ba4a69)

When you seperate RGB graphs you will usually find quite quickly dead spaces/clippings. While these could be corrected manually it's more fun to automate. 

![image](https://github.com/user-attachments/assets/c3fa7c97-75a8-45f5-8d14-20a24d8169d5)

Here is the RED channel of the same image. 

You can notice:
- On the left (dark side) first empty values then values that are too full.
- On the right, a clipping (or spike) that often happens with low-quality cameras.

I'm also colorblind which makes all this the more fun; I don't need to see colors as well as others to notice improvements.

So there you have another challenge...

1. Detect clippings (Unusual spike at the edges often happen, on the right side in this case)
2. Understand shifts (over or underexposure of a colour, or totally missing/full) > correct to a valid entry point.
3. Determine this entry point using a threshold (like a range that is 'healthy' for correction)
