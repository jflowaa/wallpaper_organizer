# Wallpaper Organizer #

This script goes through folders starting from a root. It'll look for images with a jpg or png extension. If one is found a string will be created like the following:

>> wallpaper_1920x1080_20.jpg

>Where `1920x1080` is the resolution and `20` is a random number to avoid naming conflicts.

This string is used to rename the image. 

This script also hashes the images found. If an image is hashed and that hash is already cached, then that image will be removed. The hashing is very simple and will only be able to match images that are completely the same. 

To run this program:

> python wallpaper_organizer.py `path/of/root/folder` `top`

Where `top` is the top range of numbers. Besure this number is higher than the total number of pictures. These numbers will be pulled from a pool of numbers to build the strings for the image names.


**Required Libraries**

Pillow (2.9.0)

> pip install Pillow

To install
