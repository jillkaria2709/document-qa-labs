import chromadb
# Initialize Chroma client
client = chromadb.Client()

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Create a collection
collection = client.create_collection("test_collection")
# Add some data to the collection
collection.add(
    documents=["Hello, how are you?", "What is the weather today?"],
    ids=["doc1", "doc2"]
)
# Check if the collection works
results = collection.get(ids=["doc1", "doc2"])
# Print the results
print(results)