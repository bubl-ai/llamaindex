I'm convinced that the most effective way to learn is through hands-on experiments. Engaging with actual code allows you to grasp how things function and assess the strengths and weaknesses of various options and approaches.

In the next examples we cover topics related to using LLMs with [llama-index](https://docs.llamaindex.ai/en/stable/), including:
- **Loading Data:** Processing and ingesting data.
- **Indexing:** Creating data structures for LLM querying.
- **Querying:** Making prompt calls to an LLM.

These examples were inspired by the [LlamaIndex Bottoms-Up Development video series](https://docs.llamaindex.ai/en/stable/getting_started/discover_llamaindex.html).

The goal of the examples in this folder is to utilize the **bubl-ai** environment ([container](https://github.com/bubl-ai/llamaindex-project/tree/main/docker) + [library](https://github.com/bubl-ai/llamaindex-project/tree/main/bubls/bubls)) to experiment with ideas and simultaneously learn [llama-index](https://docs.llamaindex.ai/en/stable/).

The synthetic dataset employed in these examples is the **Williams Family Tree**:
- [bubl-ai post describing the dataset](https://bubl-ai.com/posts/Data-for-evaluating-different-RAGs/)
- [Code that creates the dataset](https://github.com/bubl-ai/llamaindex-project/blob/main/builders/family_tree_synthetic_data/williams_family.py)
- [Available on our Hugging Face site](https://huggingface.co/datasets/bubl-ai/williams_family_tree)
