import os
import chromadb

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from IPython.display import Markdown, display


class ConfigurableChromaIndex:
    """Create a configurable Chroma index."""

    def __init__(self, name_collection: str, path: str, embedding_model: str):
        # create client and a new collection
        db = chromadb.PersistentClient(
            path=os.path.join(os.environ["WORKDIR"], "chroma_db")
        )
        chroma_collection = db.get_or_create_collection(name_collection)

        # define embedding function
        # embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

        # load documents
        documents = SimpleDirectoryReader(
            os.path.join(os.environ["WORKDIR"], path)
        ).load_data()

        # set up ChromaVectorStore and load in data
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,  # , embed_model=embed_model
        )

        # Query Data
        query_engine = index.as_query_engine()
        response = query_engine.query("What did the author do growing up?")
        display(Markdown(f"<b>{response}</b>"))

        # save to disk

        # index = VectorStoreIndex.from_vector_store(
        #     vector_store,
        #     embed_model=embed_model,
        # )


if __name__ == "__main__":
    a = ConfigurableChromaIndex("aaa", "/data/williams_family/biographies")
