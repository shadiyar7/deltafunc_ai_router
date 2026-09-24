from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

print("Initializing Qdrant In-Memory Vector DB for Competitor Analysis...")

client = QdrantClient(":memory:")
model = SentenceTransformer('all-MiniLM-L6-v2')

if not client.collection_exists("competitor_offers"):
    client.create_collection(
        collection_name="competitor_offers",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

mock_offers = [
    {"id": 1, "text": "Keto Diet Pills - Lose 10kg in 2 weeks! Works best in IT and ES.", "category": "Nutra"},
    {"id": 2, "text": "Crypto Auto Trader - Guaranteed 500% ROI. Hot in DE.", "category": "Crypto"},
    {"id": 3, "text": "Dating App for Singles over 40. High conversion in US.", "category": "Dating"}
]

print("Embedding and storing competitor offers in Vector DB...")
points = []
for offer in mock_offers:
    vector = model.encode(offer["text"]).tolist()
    points.append(PointStruct(id=offer["id"], vector=vector, payload=offer))

client.upsert(
    collection_name="competitor_offers",
    points=points
)

query = "What Nutra diet offers are competitors running in Italy?"
print(f"\nQuery: {query}")
query_vector = model.encode(query).tolist()

hits = client.query_points(
    collection_name="competitor_offers",
    query=query_vector,
    limit=1
).points

for hit in hits:
    print(f"RAG Match Found: {hit.payload['text']} (Score: {hit.score})")
