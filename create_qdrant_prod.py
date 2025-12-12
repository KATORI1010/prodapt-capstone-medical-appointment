from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from config import settings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)
client = QdrantClient(url=str(settings.QDRANT_URL), api_key=settings.QDRANT_API_KEY)
client.create_collection(collection_name="resumes", vectors_config=VectorParams(size=3072, distance=Distance.COSINE))
client.close()