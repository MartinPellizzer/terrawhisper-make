import json
import random

import chromadb
from chromadb.utils import embedding_functions

from lib import g

collection_name = 'medicinal-plant'

db_path = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/chroma'
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device='cuda',
)
chroma_client = chromadb.PersistentClient(path=db_path)

def retrieve_docs(query, n_results):
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef,
    )
    results = collection.query(query_texts=[query], n_results=n_results)
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    return documents, metadatas

def docs_get(query):
    n_results = 100
    documents, metadatas = retrieve_docs(
        query, 
        n_results=n_results
    )
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    researches_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        document = ' '.join(document.split(' ')[:4000])
        # print(document)
        # print(query)
        if query.lower().strip() in document.lower().strip():
            # print('true')
            # print(document)
            # print(metadata)
            research = {
                'metadata': metadata,
                'document': document,
            }
            researches_filtered.append(research)
        else:
            # print('')
            pass
        # quit()
    return researches_filtered
