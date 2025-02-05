from pinecone import Pinecone, ServerlessSpec
import time
import os

pc_database = None


def getDatabase():
    pine_cone_key = os.getenv("PINECONE_API_KEY")
    
    global pc_database 
    
    if pc_database is None:
        pc_database = Pinecone(api_key = pine_cone_key)

    return pc_database

def getDatabaseIndex(index_name):
    
    local_db = getDatabase()
    
    if not local_db.has_index(index_name):
        local_db.create_index(
            name=index_name,
            dimension=384, # Replace with your model dimensions
            metric="cosine", # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
    
    while not local_db.describe_index(index_name).status['ready']:
        time.sleep(1)

    index = local_db.Index(index_name)
    return index


