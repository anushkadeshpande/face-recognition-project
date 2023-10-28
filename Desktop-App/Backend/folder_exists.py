import os

def folder_exists(path):
    if not os.path.exists(path):
         os.makedirs(path)
    return path