from llama_parse import LlamaParse
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
)

lyft_10k = {
    "download_data": {
        "source_urls": [
            "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/lyft_2021.pdf"
        ],
        "file_names": ["lyft_10k_2021.pdf"],
    },
    "load_data": {
        "source": "local",
        # "file_extractor": {".pdf": LlamaParse(result_type="text")}
    },
    "gen_llm_eval_data": {
        "docs_pct_sample": 0.1,
        "num_questions_per_chunk": 2,
    },
    "gen_nodes": {
        "transformations": [
            SentenceSplitter(
                chunk_size=2**10,
                chunk_overlap=2**3,
            ),
            # TitleExtractor(nodes=2),
            # QuestionsAnsweredExtractor(questions=1),
            # SummaryExtractor(summaries=["prev", "self"]),
            # KeywordExtractor(keywords=5),
        ]
    },
    "gen_qa_pairs": {
        "nodes_pct_sample": 0.3,
        "num_questions_per_chunk": 2,
    },
    "gen_index": {},
    "gen_query_engine": {"similarity_top_k": 5},
    "gen_retriever": {},
    "gen_chat_engine": {},
}

papers_ridesharing = {
    "download_data": {
        "source_urls": [
            "https://arxiv.org/pdf/2202.07086",
            "https://arxiv.org/pdf/2403.13083",
            "https://arxiv.org/pdf/2405.02835",
            "https://arxiv.org/pdf/2402.01644",
        ],
        "file_names": [
            "price_cycles_ridesharing_platforms.pdf",
            "rideshare_system_as_stable_matching.pdf",
            "algorithmic_collusion_rideshare_example.pdf",
            "carbon_reduction_ridesharing.pdf",
        ],
    },
    "load_data": {
        "source": "local",
    },
    "gen_llm_eval_data": {
        "docs_pct_sample": 0.2,
        "num_questions_per_chunk": 1,
    },
    "gen_nodes": {},
    "gen_qa_pairs": {
        "nodes_pct_sample": 0.2,
        "num_questions_per_chunk": 1,
    },
    "gen_index": {},
    "gen_query_engine": {"similarity_top_k": 5},
    "gen_retriever": {},
    "gen_chat_engine": {},
}

wiki_public_companies = {
    "load_data": {
        "source": "wikipedia",
        "pages": [
            "Lyft Company",
            "Uber Company",
            "Airbnb Company",
            "Microsoft Company",
            "Apple_Inc Company",
            "Nvidia Company",
            "Amazon Company",
        ],
    },
    "gen_llm_eval_data": {
        "docs_pct_sample": 0.5,
        "num_questions_per_chunk": 2,
    },
    "gen_nodes": {},
    "gen_qa_pairs": {
        "nodes_pct_sample": 0.5,
        "num_questions_per_chunk": 2,
    },
    "gen_index": {},
    "gen_query_engine": {"similarity_top_k": 5},
    "gen_retriever": {},
    "gen_chat_engine": {},
}
