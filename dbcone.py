from pinecone import Pinecone, ServerlessSpec
import time
import os

global pc_database


def getDatabase():
    pine_cone_key = os.getenv("PINECONE_API_KEY")
    
    if pc_database is None:
        pc_database = Pinecone(api_key = pine_cone_key)

    return pc_database

def getDatabaseIndex(index_name):
    
    getDatabase()
    
    if not pc_database.has_index(index_name):
        pc_database.create_index(
            name=index_name,
            dimension=384, # Replace with your model dimensions
            metric="cosine", # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
    
    while not pc_database.describe_index(index_name).status['ready']:
        time.sleep(1)

    index = pc_database.Index(index_name)
    return index


