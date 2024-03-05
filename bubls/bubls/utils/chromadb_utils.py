from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import os
import chromadb


class ConfigurableChromaIndex:
    """Create a configurable Chroma index.
    We will be including more complex functionalities
    to this class like:
    - Embedding model
    - Loading from Disk
    - Different configurations with the objective of testing performance
    """

    def __init__(self, name_collection: str, path: str):
        # create client and a new collection
        db = chromadb.PersistentClient(
            path=os.path.join(os.environ["WORKDIR"], "chroma_db")
        )
        chroma_collection = db.get_or_create_collection(name_collection)

        # load documents
        documents = SimpleDirectoryReader(
            os.path.join(os.environ["WORKDIR"], path)
        ).load_data()

        # set up ChromaVectorStore and load in data
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,  # , embed_model=embed_model
        )


if __name__ == "__main__":
    chroma_index = ConfigurableChromaIndex(
        "collection_xyz",
        "data/williams_family/biographies",
    )
