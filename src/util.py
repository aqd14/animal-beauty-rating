import os

import os
path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data')

def rename(animal_type):
    data_file_path = os.path.join(path, animal_type)
    files = os.listdir(data_file_path)
    for file in files:
        os.rename(os.path.join(data_file_path, file), os.path.join(data_file_path, animal_type + '_' + file))

animal_types = ['bird', 'cat', 'cow', 'dog', 'frog', 'horse']
for animal_type in animal_types:
    rename(animal_type)