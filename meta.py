import os
import time
import metapub

from urllib.request import urlretrieve
import json

from lib import g
from lib import io

proj = 'ozonogroup'
# query = 'ozone'
query = 'listeria'

proj = 'terrawhisper'
query = 'medicinal_plants'

abstracts_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'
pdfs_done_path = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/pdfs-done'
pdfs_fail_path = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/pdfs-fail'

try: os.makedirs(f'{pdfs_done_path}')
except: pass
try: os.makedirs(f'{pdfs_fail_path}')
except: pass

pmids = [filename.split('.')[0] for filename in os.listdir(abstracts_folderpath)]
pmids_done = [filename.split('.')[0] for filename in os.listdir(pdfs_done_path)]
pmids_fail = [filename.split('.')[0] for filename in os.listdir(pdfs_fail_path)]

tot_num = 0
for i, pmid in enumerate(pmids):
    print(f'{i+1}/{len(pmids)} - {pmid}')
    if pmid in pmids_done: continue
    if pmid in pmids_fail: continue
    try: 
        src = metapub.FindIt(pmid)
    except:
        io.file_write(f'{pdfs_fail_path}/{pmid}', '')
        continue
    print(src.pma.title)
    if src.url:
        try:
            urlretrieve(src.url, f'{pdfs_done_path}/{pmid}.pdf')
        except:
            io.file_write(f'{pdfs_fail_path}/{pmid}.pdf', '')
    else:
        io.file_write(f'{pdfs_fail_path}/{pmid}.txt', '')
        print(src.reason)
    print()

    time.sleep(1)
    tot_num += 1
    if tot_num >= 1000:
        tot_num = 0
        time.sleep(600)

