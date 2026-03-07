import os
import json

import chromadb
from chromadb.utils import embedding_functions

from lib import io

AUTHOR_NAME = 'Leen Randell'

proj = 'terrawhisper'
collection_name = 'medicinal-plant'

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
db_path = f'{vault}/{proj}/studies/chroma'

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device='cuda',
)
chroma_client = chromadb.PersistentClient(path=db_path)
collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=sentence_transformer_ef)
documents_folderpath = f'{vault}/{proj}/studies/pubmed/{collection_name}/json'
documents_filenames = os.listdir(documents_folderpath)
for i, document_filename in enumerate(documents_filenames):
    print(f'{i}/{len(documents_filenames)}')
    document_filepath = f'{documents_folderpath}/{document_filename}'
    try: data = io.json_read(document_filepath)
    except: continue
    try: article = data['PubmedArticle'][0]['MedlineCitation']['Article']
    except: continue
    try: abstract_text = article['Abstract']['AbstractText']
    except: continue
    try: journal_title = article['Journal']['Title']
    except: continue
    abstract_text = ' '.join(abstract_text).replace('  ', ' ')
    pmid = document_filename.split('.')[0]
    metadata = {
        'pmid': pmid,
        'journal_title': journal_title,
    }
    collection.add(
        documents=[abstract_text],
        metadatas=[metadata],
        ids=[pmid],
    )
results = collection.query(query_texts=['test'], n_results=5)
print(results)
