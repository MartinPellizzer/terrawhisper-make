import os
import time
import shutil

from lib import g
from lib import io
from lib import llm

def folder_copy():
    source_foldername = 'drduke'
    input_foldername = 'normalize'
    output_foldername = 'resolve'
    ###
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    input_filenames = os.listdir(input_folderpath)
    i = 0
    for input_filename in input_filenames[i:]:
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        shutil.copy(input_filepath, output_filepath)
    
def run():
    print('RESOLVE >> drduke')

    start = time.perf_counter()
    ### TODO: temp function: remove when implement real function
    folder_copy()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

