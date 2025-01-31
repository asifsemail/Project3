from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv, find_dotenv
from dbcone import getDatabase
from dbcone import getDatabaseIndex
import os
import uuid
import pandas as pd
import numpy as np

global sentence_model

def initial():
    load_dotenv(find_dotenv('Keys.env'))
    initialize_model()
    getDatabase()
    return True

def initialize_model():
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_model():
    if sentence_model is None:
        initialize_model()
    return sentence_model

def get_sentence_embedding(sentence):
    model = get_model()
    return model.encode(sentence)

def read_files(inputDir, outputDir, topic=None):
    
    files = os.listdir(inputDir)
    
    if topic is None:
        topic = os.path.basename(inputDir)
    
    embeded_lst = []
    
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(inputDir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    text = f.read()
                    embedding = get_sentence_embedding(text)
                    f.close()
                    os.rename(file_path, os.path.join(outputDir, file))
                    
                    embeded_lst.append(
                        {
                            "id" : str(uuid.uuid4().hex),
                            "topic": topic,
                            "metadata": {'text':text},
                            "embedding": embedding.tolist()
                        }
                    )

    return embeded_lst

def save_to_database(embeded_lst, index_name = 'test_videos' ,namespace="sample-namespace"):
    
    db_index = getDatabaseIndex(index_name)
    
    db_index.upsert(
        vectors=embeded_lst,
        namespace=namespace
    )    

def fetch_from_database(search_text, top_k = 5, index_name = 'test_videos' ,namespace="sample-namespace"):
    
    db_index = getDatabaseIndex(index_name)
    
    results = db_index.query(namespace=namespace,
        vector=np.array(get_sentence_embedding(search_text)).tolist(),
        top_k=top_k,
        include_values=True
    )
    
    return results

def embed_text_files(inputDir, outputDir, topic):
    return read_files(inputDir=inputDir, outputDir=outputDir, topic=topic)

def main():
    inputDir = 'inputDir'
    outputDir = 'outputDir'
    topic = 'test'
    
    embeded_lst = embed_text_files(inputDir, outputDir, topic)
    save_to_database(embeded_lst)
    
    fetch_from_database('This is test sentence')


if __name__ == "__main__":
    main()