from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv, find_dotenv
from dbcone import getDatabase
from dbcone import getDatabaseIndex
import os
import uuid
import pandas as pd
import numpy as np
from pathlib import Path
from summary import generate_combined_summary_and_key_points

sentence_model = None
inputDir = None
outputDir = None
topic = None
db_index_name = None
db_namespace_name = None



def initialize_model():
    global sentence_model
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_model():
    if sentence_model is None:
        initialize_model()
    return sentence_model

def get_sentence_embedding(sentence):
    model = get_model()
    return model.encode(sentence)

def getOutputDir(outputDirectory):
    
    outputDir = Path(outputDirectory)
    
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    return outputDir
    
def read_files(inputDirectory, outputDirectory, topic=None):
    
    inputDir = Path(inputDirectory)
    
    embeded_lst = []
    
    if ( (not os.path.exists(inputDir)) or (not os.path.isdir(inputDir)) ):
        return embeded_lst
    
    files = os.listdir(inputDir)
    
    if topic is None:
        topic = os.path.basename(inputDir)

    if len(files) <= 0:
        return embeded_lst
    
    outputDir = getOutputDir(outputDirectory)
    
    textfile = "" 

    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(inputDir, file)
            
            if os.path.isfile(file_path):
                
                with open(file_path, 'r') as f:
            
                    text = f.read()
                    embedding = get_sentence_embedding(text)
                    f.close()

                    if not os.path.isfile(os.path.join(outputDir, file)):
                        os.rename(file_path, os.path.join(outputDir, file))
                    else:
                        os.remove(file_path)
                        
                    (topic_gen, summary, keypoints) = generate_combined_summary_and_key_points(text)
                    
                    if (topic_gen is not None): 
                        topic = topic_gen
                    
                    embeded_lst.append(
                        {
                            "id" : str(uuid.uuid4().hex),
                            "metadata": {
                                'text':text,
                                "topic": topic,
                                "summary": summary,
                                "keypoints":keypoints
                                },
                            "values": embedding.tolist()
                        }
                    )
                    
                    textfile += "\n" + text 

    (topic_gen1, summary1, keypoints1) = generate_combined_summary_and_key_points(textfile)
    
    input_data = {
        'summary' : summary1,
        'keypoints' : keypoints1
    }
    
    return input_data, embeded_lst

def save_to_database(embeded_lst, index_name = 'test_videos' ,namespace="sample-namespace"):
    
    if len(embeded_lst) > 0 :
        db_index = getDatabaseIndex(index_name)
        
        db_index.upsert(
            vectors=embeded_lst,
            namespace=namespace
        )    


def embed_text_files(inputDir, outputDir, topic):
    
    return read_files(inputDirectory=inputDir, outputDirectory=outputDir, topic=topic)

def configureApp():
    
    global inputDir, outputDir, topic, db_index_name, db_namespace_name
    
    currPath = Path.cwd()
    
    inputDir = os.path.join( currPath, 'output')
    outputDir = os.path.join(currPath, 'processed')
    
    topic = 'test'
    db_index_name = 'samplevideos'
    db_namespace_name="video-namespace"
        
    load_dotenv(find_dotenv('Keys.env'))
    initialize_model()
    getDatabase()
    
    return True

def fetch_from_database(search_text, topics =[] ,top_k = 5, index_name = 'test-videos' ,namespace="sample-namespace"):
    
    db_index = getDatabaseIndex(index_name)
    
    results = db_index.query(namespace=namespace,
        vector=np.array(get_sentence_embedding(search_text)).tolist(),
        top_k=top_k,
        include_values=True,
        include_metadata=True,    
          
    )
    
    return results

def captureData():
    
    global inputDir, outputDir, topic, db_index_name, db_namespace_name

    input_data, embeded_lst = embed_text_files(inputDir, outputDir, topic)
    
    save_to_database(embeded_lst, index_name =db_index_name, namespace=db_namespace_name)
    
    return input_data

def queryRepository(search_text):
    
    global db_index_name, db_namespace_name
    
    result = fetch_from_database(search_text, index_name = db_index_name, namespace=db_namespace_name)

    print(f'Results: {result}')
    

def mainApp():
    
    configureApp()
    input_data = captureData()
    return input_data
    

if __name__ == "__main__":
    mainApp()
