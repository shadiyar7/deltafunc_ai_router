import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

print(f"Connecting to Qdrant at {qdrant_host}:{qdrant_port}...")

client = QdrantClient(host=qdrant_host, port=qdrant_port)
model = SentenceTransformer('all-MiniLM-L6-v2')

if not client.collection_exists("competitor_offers"):
    client.create_collection(
        collection_name="competitor_offers",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

def search_competitors(query: str):
    vector = model.encode(query).tolist()
    hits = client.query_points(
        collection_name="competitor_offers",
        query=vector,
        limit=1
    ).points
    return hits

if __name__ == '__main__':
    print("Test Search:", search_competitors("Nutra diet offers"))
