import os
import json
import time
import shutil

from lib import g
from lib import io

def folder_copy():
    source_foldername = f'powo'
    input_foldername = f'resolve'
    output_foldername = f'qualify'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_foldername}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        shutil.copy2(input_filepath, output_filepath)

def run():
    print('QUALIFY >> powo')

    start = time.perf_counter()
    folder_copy()
    print(f'folder copy() - execution time: ', time.perf_counter() - start)

