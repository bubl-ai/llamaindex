from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
import random


def load_corpus(files, pct_sample: float = 1.0, verbose=True):
    if verbose:
        print(f"Loading files {files}")

    reader = SimpleDirectoryReader(input_files=files)
    docs = reader.load_data()

    if pct_sample < 1:
        if pct_sample <= 0:
            raise ValueError("pct_sample can't be lower than zero.")
        docs = random.sample(docs, int(pct_sample * len(docs)))

    if verbose:
        print(f"Loaded {len(docs)} docs")

    parser = SentenceSplitter()
    nodes = parser.get_nodes_from_documents(docs, show_progress=verbose)

    if verbose:
        print(f"Parsed {len(nodes)} nodes")

    return nodes
