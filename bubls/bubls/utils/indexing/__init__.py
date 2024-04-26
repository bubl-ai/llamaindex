import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from typing import Optional, Dict
from llama_index.core.readers.base import BaseReader


def create_index_from_path(
    persist_dir: str,
    data_dir: Optional[str] = None,
    file_extractor: Optional[Dict[str, BaseReader]] = None,
) -> VectorStoreIndex:
    """Create an index with the provided parameters.

    Args:
        persist_dir (str): Where the index is persisted. If the index was already
            created before, it is loaded without creating it again.
        data_dir (Optional[str], optional): Path where the data to be indexed is stored.
            Defaults to None.
        file_extractor (Optional[Dict[str, BaseReader]], optional): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. If not specified, use default from DEFAULT_FILE_READER_CLS

    Returns:
        VectorStoreIndex: Index created from the provided directoryand file_extractor.
    """
    if not os.path.exists(persist_dir):
        print("Creating Index")
        if not data_dir:
            raise ValueError(
                "If creating a new index data_dir must be provided."
            )
        # load the documents and create the index
        documents = SimpleDirectoryReader(
            data_dir, file_extractor=file_extractor
        ).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=persist_dir)
    else:
        print("Loading Index")
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)

    return index
