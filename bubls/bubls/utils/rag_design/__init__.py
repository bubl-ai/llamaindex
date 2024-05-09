from bubls.utils.data.download import download_file_from_url
from bubls.utils.evaluation.evaluate_embeddings import evaluate_embed_model
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.core.evaluation import (
    DatasetGenerator,
    EmbeddingQAFinetuneDataset,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.finetuning import generate_qa_embedding_pairs
from llama_index.readers.wikipedia import WikipediaReader
from typing import Any, Dict
import pickle
import random
import os


class RAGBuilder:
    def __init__(self, components_cfg: dict):
        self.components_cfg = components_cfg
        self.documents = {}
        self.llm_eval_data = {}
        self.nodes = {}
        self.qa_pairs = {}

    def ingest_data(self, c_id: str):
        component_cfg = self.components_cfg[c_id]

        # Nodes is the main output, check if exists
        nodes_data_path = os.path.join(
            os.environ["PERSIST_DIR"], c_id, "nodes", "nodes.pkl"
        )
        if not os.path.exists(nodes_data_path):
            print(f"Generating data artifacts for {c_id}")
            self._download_data(c_id, component_cfg.get("download_data"))
            self._load_data(c_id, component_cfg.get("load_data"))
            self._gen_llm_eval_data(
                c_id, component_cfg.get("gen_llm_eval_data", {})
            )
            self._gen_nodes(c_id, component_cfg.get("gen_nodes", {}))
            self._gen_qa_pairs(c_id, component_cfg.get("gen_qa_pairs", {}))
        else:
            print(f"Loading data artifacts for {c_id}")
            self._get_llm_eval_data(c_id)
            self._get_nodes(c_id)
            self.get_qa_pairs(c_id)

    def _download_data(self, c_id: str, cfg: Dict[str, Any]):
        if not cfg:
            return
        for source_url, file_name in zip(
            cfg["source_urls"], cfg["file_names"]
        ):
            save_data_to = os.path.join(os.environ["DATA_DIR"], c_id)
            download_file_from_url(
                source_url,
                file_name,
                save_data_to,
            )
            print(f"File {file_name} available at {save_data_to}")

    def _load_data(self, c_id: str, cfg: Dict[str, Any]):
        if cfg["source"] == "local":
            self._load_data_local(c_id, cfg)
        elif cfg["source"] == "wikipedia":
            self._load_data_wikipedia(c_id, cfg)
        else:
            raise ValueError(f"{cfg['source']} not supported.")

    def _load_data_local(self, c_id: str, cfg: Dict[str, Any]):
        print(f"Loading local data {c_id}")
        self.documents[c_id] = SimpleDirectoryReader(
            os.path.join(os.environ["DATA_DIR"], c_id),
            file_extractor=cfg.get("file_extractor", {}),
        ).load_data()

    def _load_data_wikipedia(self, c_id: str, cfg: Dict[str, Any]):
        print(f"Loading wikipedia data {c_id}")
        reader = WikipediaReader()
        self.documents[c_id] = reader.load_data(pages=cfg["pages"])

    def _gen_llm_eval_data(self, c_id: str, cfg: Dict[str, Any]):
        persist_dir = os.path.join(
            os.environ["PERSIST_DIR"], c_id, "llm_eval_data"
        )
        data_path = os.path.join(persist_dir, f"llm_eval_data.pkl")
        os.makedirs(persist_dir, exist_ok=True)
        print(f"Generating LLM Eval Data for {c_id}")
        sample = int(
            cfg.get("docs_pct_sample", 0.2) * len(self.documents[c_id])
        )
        sample = sample if sample > 0 else 1
        sampled_docs = random.sample(self.documents[c_id], sample)

        data_generator = DatasetGenerator.from_documents(
            sampled_docs,
            num_questions_per_chunk=cfg.get("num_questions_per_chunk", 2),
        )

        self.llm_eval_data[c_id] = (
            data_generator.generate_questions_from_nodes()
        )

        with open(data_path, "wb") as file:
            pickle.dump(self.llm_eval_data[c_id], file)

    def _get_llm_eval_data(self, c_id: str):
        persist_dir = os.path.join(
            os.environ["PERSIST_DIR"], c_id, "llm_eval_data"
        )
        data_path = os.path.join(persist_dir, f"llm_eval_data.pkl")
        print(f"Loading LLM eval data for {c_id}")
        with open(data_path, "rb") as file:
            self.llm_eval_data[c_id] = pickle.load(file)

    def _gen_nodes(self, c_id: str, cfg: Dict[str, Any]):
        print(f"Generating Nodes for {c_id}")
        persist_dir = os.path.join(os.environ["PERSIST_DIR"], c_id, "nodes")
        data_path = os.path.join(persist_dir, "nodes.pkl")
        os.makedirs(persist_dir, exist_ok=True)

        ## Using node_parser
        # node_parser = SentenceSplitter(**cfg)
        # self.nodes[c] = node_parser.get_nodes_from_documents(
        #     self.documents[c], show_progress=False
        # )

        ## Using transformation pipeline
        transformations = cfg.get("transformations", [SentenceSplitter()])
        pipeline = IngestionPipeline(transformations=transformations)
        self.nodes[c_id] = pipeline.run(documents=self.documents[c_id])

        with open(data_path, "wb") as file:
            pickle.dump(self.nodes[c_id], file)

    def _get_nodes(self, c_id: str):
        print(f"Loading Nodes for {c_id}")
        persist_dir = os.path.join(os.environ["PERSIST_DIR"], c_id, "nodes")
        data_path = os.path.join(persist_dir, "nodes.pkl")
        print(f"Loading nodes {c_id}")
        with open(data_path, "rb") as file:
            self.nodes[c_id] = pickle.load(file)

    def _gen_qa_pairs(self, c_id: str, cfg: Dict[str, Any]):
        print(f"Generating QA Pairs for {c_id}")
        persist_dir = os.path.join(os.environ["PERSIST_DIR"], c_id, "qa_pairs")
        data_path = os.path.join(persist_dir, "qa_pairs.json")
        os.makedirs(persist_dir, exist_ok=True)
        sample = int(cfg.get("nodes_pct_sample", 0.2) * len(self.nodes[c_id]))
        sample = sample if sample > 0 else 1
        sampled_nodes = random.sample(self.nodes[c_id], sample)

        self.qa_pairs[c_id] = generate_qa_embedding_pairs(
            llm=Settings.llm,
            nodes=sampled_nodes,
            num_questions_per_chunk=cfg.get("num_questions_per_chunk", 2),
        )
        self.qa_pairs[c_id].save_json(data_path)

    def get_qa_pairs(self, c_id: str):
        print(f"Loading QA pairs for {c_id}")
        persist_dir = os.path.join(os.environ["PERSIST_DIR"], c_id, "qa_pairs")
        data_path = os.path.join(persist_dir, "qa_pairs.json")
        self.qa_pairs[c_id] = EmbeddingQAFinetuneDataset.from_json(data_path)

    def build(self):
        for c_id, component_cfg in self.components_cfg.items():
            self.ingest_data(c_id)
            # self._set_index(c)
            # self._set_query_engine(c)
            # self._set_retriever(c)
            # self._set_chat_engine(c)
