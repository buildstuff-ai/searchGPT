from sqlite3 import DatabaseError
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

def get_chromadb_collection():
    """
    Validates the connection to the chromadb server and returns the collection
    """
    try:
        # docker run -d -p 8000:8000 chromadb/chromadb
        client = chromadb.HttpClient(host=os.getenv('CHROMA_HOST'), port=8000)
            
        collection = client.get_or_create_collection(name="searchgpt",
                                                     metadata={"hnsw:space": "cosine"})
        return collection
    except DatabaseError as e:
        raise DatabaseError(f"Error in getting collection: {e}")
    

if __name__ == "__main__":
    print(get_chromadb_collection())
