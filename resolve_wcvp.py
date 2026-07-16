import os
import time
import shutil

from lib import g
from lib import io
from lib import llm

import pipeline_utils

def folder_copy():
    source_foldername = 'wcvp'
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
    print('RESOLVE >> wcvp')

    start = time.perf_counter()
    ### NO RESOLVE NEEDED FOR NOT (WCVP IS GROUND TRUTH)
    # folder_copy()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

    ### WCVP DISTRIBUTION
    start = time.perf_counter()
    pipeline_utils.folder_copy(
        input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/wcvp/distribution',
        output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/wcvp/distribution',
    )
    print(f'wcvp distribution() - execution time: ', time.perf_counter() - start)

