import os
import json
import time
import shutil

from lib import g
from lib import io

def folder_copy():
    input_foldername = f'observe'
    output_foldername = f'qualify'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
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

print('QUALIFY >> pubmed')

start = time.perf_counter()
folder_copy()
print(f'folder_copy() - execution time: ', time.perf_counter() - start)

