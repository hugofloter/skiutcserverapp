import os
import string
import random

from config import IMAGES_SOURCE
from utils.errors import Error


def savefile(file, category):
    name, ext = os.path.splitext(file.filename)

    if ext not in ('.png', '.jpg', '.jpeg'):
        return Error('Not an image', 400).get_error()

    save_path = f"{IMAGES_SOURCE}/{category}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    letters = string.ascii_lowercase
    file_name = ''.join(random.choice(letters) for i in range(8))
    file_path = f"{save_path}/{file_name}{ext}"

    file.save(file_path)

    return { 'img_url': f'/{category}/{file_name}{ext}' }
