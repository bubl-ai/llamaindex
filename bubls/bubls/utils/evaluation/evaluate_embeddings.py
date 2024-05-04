from llama_index.core.llama_dataset.legacy.embedding import (
    EmbeddingQAFinetuneDataset,
)
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
from tqdm.notebook import tqdm
from typing import List
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pandas as pd


def get_query_hit_pairs(
    dataset: EmbeddingQAFinetuneDataset,
    embed_model,
    top_k: int = 5,
    verbose: bool = False,
) -> pd.DataFrame:
    """Dataset contains
    - queries
    - relevant node for each query
    - all nodes in dataset

    We first create an index from the embed model. Then, for all queries,
    we get the top k retrieved nodes from the model. Then we check if the
    relevant node is in the retrieved ones.

    Args:
        dataset (EmbeddingQAFinetuneDataset): Dataset to evaluate generated from
            EmbeddingQAFinetuneDataset.
        embed_model (_type_): Model to be used for creating embeddings
        top_k (int, optional): How many nodes to retrieve. Defaults to 5.
        verbose (bool, optional): Show progress. Defaults to False.

    Returns:
        pd.DataFrame: Each row has information of a query and if
            it was a hit or not
    """
    corpus = dataset.corpus
    queries = dataset.queries
    relevant_docs = dataset.relevant_docs

    nodes = [TextNode(id_=id_, text=text) for id_, text in corpus.items()]
    index = VectorStoreIndex(
        nodes, embed_model=embed_model, show_progress=verbose
    )
    retriever = index.as_retriever(similarity_top_k=top_k)

    eval_results = []
    for query_id, query in tqdm(queries.items()):
        retrieved_nodes = retriever.retrieve(query)
        retrieved_ids = [node.node.node_id for node in retrieved_nodes]
        expected_id = relevant_docs[query_id][0]
        is_hit = expected_id in retrieved_ids

        eval_result = {
            "is_hit": is_hit,
            "retrieved": retrieved_ids,
            "expected": expected_id,
            "query": query_id,
        }
        eval_results.append(eval_result)
    return pd.DataFrame(eval_results)


def sentence_transformer_ir_evaluator(
    dataset: EmbeddingQAFinetuneDataset,
    model_id: str,
    name: str,
) -> InformationRetrievalEvaluator:
    """
    Given a set of queries and a large corpus set. It will retrieve for each query
    the top-k most similar document. It measures Mean Reciprocal Rank (MRR), Recall,
    and Normalized Discounted Cumulative Gain (NDCG).

    Only works for sentencetransformers compatible models.

    Args:
        dataset (EmbeddingQAFinetuneDataset):  Dataset to evaluate generated from
            EmbeddingQAFinetuneDataset.
        model_id (str): Sentence Transformer model id.
        name (str): Name given to the evaluator

    Returns:
        InformationRetrievalEvaluator: evaluator.
    """
    corpus = dataset.corpus
    queries = dataset.queries
    relevant_docs = dataset.relevant_docs

    evaluator = InformationRetrievalEvaluator(
        queries, corpus, relevant_docs, name=name
    )
    model = SentenceTransformer(model_id)
    output_path = "results/"
    Path(output_path).mkdir(exist_ok=True, parents=True)

    return evaluator(model, output_path=output_path)
