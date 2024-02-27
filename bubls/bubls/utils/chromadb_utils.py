import os
import chromadb


def collection_from_folder():
    # client = chromadb.PersistentClient(path="/llamaindexproject")
    client = chromadb.PersistentClient(
        path=os.path.join(os.environ["PWD"], "chroma_collections")
    )
    # Create a collection
    collection = client.get_or_create_collection(name="my_collection22")
    collection.add(
        documents=[
            "This is a document galileo figaro magnifico hey there is someone playing videogames down on the road smiling at everyone",
            "This is another document",
        ],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"],
    )

    # some useful methods
    collection.peek()  # returns a list of the first 10 items in the collection
    collection.count()  # returns the number of items in the collection


collection_from_folder()
