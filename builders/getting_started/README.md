Example gotten from [llamaindex documentation](https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html)

How to use:
```
python starter.py
```

## What is LlamaIndex?

LlamaIndex provides abstractions to make the ingestion, structuring, and access of data more straightforward, enabling seamless integration into Large Language Models (LLMs) for more accurate text generation.

While LLMs are trained on extensive datasets, they lack training on private or domain-specific data. Fine-tuning a LLM with your data is costly, making it challenging to keep the model up-to-date with the latest information. Additionally, it often lacks observability.[LINK](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html#)

## What is RAG?

Retrieval-Augmented Generation (RAG) provides an alternative1. This technique focuses on context augmentation to achieve more precise text generation tailored to your specific data.

Key steps in RAG implementation:

- **Get Information**: Nodes serve as the atomic unit of data, and connectors assist in ingesting these nodes.

- **Index and Add to Query as Context**: This involves generating vector embeddings and incorporating them into your query as context.

- **Pass Improved Prompt to LLM**: Further details will be covered in upcoming posts, addressing querying, retrievers, routers, postprocessors, and synthesizers.

The beauty of RAG lies in its absence of training, ensuring it's always up-to-date by adding your data to the existing data accessible to LLMs. Another vital aspect is the ability to store your indexes, mainly accomplished through specialized databases known as vector stores. Finally a RAG framework must effectively perform proper evaluation on the accuracy of the responses.[LINK](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html)

## LlamaIndex Tools

- **Data Connectors**: Facilitate data ingestion.

- **Data Indexes**: Provide representations of the data usable in LLMs.

- **Engines**: Serve as end-to-end pipelines for interaction with LLMs.

- **Data Agents**: LLM-based decision-makers offering flexibility to tackle complex problems.

- **Application Integrations**: Enable seamless integration of LlamaIndex into other frameworks.
