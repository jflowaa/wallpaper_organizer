from PIL import Image
from random import choice
import argparse
import os
import re
import hashlib


def make_image_name(folder, imagename, number, extension):
    """
    Creates a string like the following:
        wallpaper_1920x1080_20.jpg
    Where the resolution is taken from the image and a number
    is added to have non-conflicting imageames
    """
    path = "{}/{}".format(folder, imagename)
    res = str(Image.open(path).size).replace(" ", "").replace(",", "x")
    res = re.sub('[()]', '_', res)
    new_imagename = "wallpaper{}{}.{}".format(res, str(number), extension)
    return new_imagename


def rename_image(folder, imagename, new_imagename, extension):
    """
    Takes the newly created imagename and replaces the old imagename.
    extension is passed incase of a rename conflict.
    """
    while True:
        try:
            os.rename("{}/{}".format(folder, imagename),
                      "{}/{}".format(folder, new_imagename))
            print("Renaming image-> {}  To-> {}".format(imagename,
                                                        new_imagename))
            break
        except FileExistsError:
            number = get_number_from_pool()
            new_imagename = make_image_name(folder, new_imagename,
                                            number, extension)
    return


def check_if_renamed(imagename):
    name_regex = re.compile('(wallpaper_)(\d*)(x)(\d*)(_)(\d*)(.\D{3,4})')
    return name_regex.match(imagename)


def hash_image(folder, imagename):
    """
    Opens the image, converts to binary, creates a hash from that.
    Checks if image has same hash as ones before, if so returns True.
    If not, adds the hash to the list and returns False.
    """
    global hash_list
    with open("{}/{}".format(folder, imagename), 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    if file_hash in hash_list:
        return True
    else:
        hash_list.append(file_hash)
    return False


def process_image(folder, imagename, number, extension):
    """
    Calls hash_image to cache its hash. If hash is already cahced, image
    is removed. If hash is not cached, a new name is generated for that image
    afterwards the image is renamed to that.
    """
    if hash_image(folder, imagename):
        print("Duplicate image found. Removing...")
        os.remove("{}/{}".format(folder, imagename))
        return False
    new_imagename = make_image_name(folder, imagename, number, extension)
    rename_image(folder, imagename, new_imagename, extension)
    return True


def build_number_pool(top):
    """
    A list is built from 0-top. Example:
    top = 10
    list = [0, 1, 2, 3, 4, 5, 6, 7, 9]
    """
    return list(range(0, top))


def tally_number_pool(pool, number):
    """
    Removes used numbers to prevent future rename conflicts
    """
    return pool.remove(number)


def get_number_from_pool():
    """
    Gets a number from the pool.
    """
    global number_pool
    number = choice(number_pool)
    tally_number_pool(number_pool, number)
    return number


def iterate_through_image(root):
    """
    Iterates through the root directory looking for image files. Images
    are hashed, the hash will be used for making sure there are no
    duplicates, duplicates will be removed. The hash is very basic,
    it'll only match images that are completely the same.
    Finally the images are renamed to a more organized fashion.
    """
    image_number = get_number_from_pool()
    for folder, subfolders, imagenames in os.walk(root):
        print("Seraching through {} for images...".format(folder))
        for imagename in imagenames:
            if check_if_renamed(imagename) is None:
                if imagename.endswith(".jpg"):
                    if process_image(folder, imagename, image_number, "jpg"):
                        image_number += 1
                if imagename.endswith(".png"):
                    if process_image(folder, imagename, image_number, "png"):
                        image_number += 1
                if imagename.endswith(".jpeg"):
                    if process_image(folder, imagename, image_number, "jpeg"):
                        image_number += 1
                if imagename.endswith(".bmp"):
                    if process_image(folder, imagename, image_number, "bmp"):
                        image_number += 1
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wallpaper library " +
                                     "organizer. Renames images and " +
                                     "removes duplicates.")
    parser.add_argument('path', type=str, help="Root directory of wallpapers")
    parser.add_argument('top', type=int, help="Generous guess of wallpapers")
    args = parser.parse_args()
    hash_list = list()
    number_pool = build_number_pool(args.top)
    iterate_through_image(args.path)
