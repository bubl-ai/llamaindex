from bubls.utils.data.download import download_folder_from_repo
from bubls.utils.indexing import create_index_from_path
from bubls.utils.agents.general_function_tools import read_code_tool
from llama_index.llms.openai import OpenAI
from llama_parse import LlamaParse
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from pydantic import BaseModel
import os
import ast


def retry(func):
    """Simple decorator for retrying."""

    def wrapper(*args, **kargs):
        max_retries = 3
        for _ in range(max_retries):
            try:
                result = func(*args, **kargs)
                return result
            except Exception as e:
                print(f"Error occured: {e}. Retrying...")
        raise RuntimeError("Max retries exceeded.")

    return wrapper


class CodeOutput(BaseModel):
    description: str
    code: str
    filename: str


class GenerateCodeFromQuery:
    def __init__(self, repo_url: str, repo_name: str, data_folder: str):
        self.data_dir = download_folder_from_repo(
            repo_url, repo_name, data_folder
        )
        self.persist_dir = os.path.join(os.environ["PERSIST_DIR"], repo_name)
        self.llm = OpenAI(model="gpt-4")

    def _create_pdf_api_tool(self) -> None:
        """Create a tool from a Query Engine that reads API's pdf."""
        parser = LlamaParse(result_type="markdown")
        index = create_index_from_path(
            self.persist_dir, self.data_dir, {".pdf": parser}
        )
        query_engine = index.as_query_engine(llm=self.llm)
        self.pdf_api_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="api_documentation",
                description="""
                    This gives documentation about code for an API.
                    Use this for reading docs for the API
                """,
            ),
        )

    def _define_tools(self) -> None:
        """List of tools to be used by the agent."""
        self.tools = [self.pdf_api_tool, read_code_tool]

    def _create_code_agent_from_tools(self) -> None:
        """Initialize the ReAct agent that generates and analyzes code."""
        context = """
            Purpose: The primary role of this agent is to assist users by analyzing code.
            It should be able to generate code and answer questions about code provided.
            Use only the tools provided and not previous knowledge.
        """
        self.agent = ReActAgent.from_tools(
            self.tools, llm=self.llm, verbose=True, context=context
        )

    def _create_query_pipeline_gen_code(self) -> None:
        """Create pipeline that takes the output of an LLM and transfroms it into a
        json object with the information defined in CodeOutput pydantic class.
        """
        parser_prompt = """
            Parse the previous previous response into:
            - A simple description.
            - Valid code as string
            - Create a valid filename for this code to be saved. 
            Here is the previous response: {previous_response}."""

        # We are telling the model that we want the code to have the pydantic format
        parser = PydanticOutputParser(CodeOutput)

        # parser_prompt + "here is json schema to follow" + CodeOutput as json
        json_prompt = parser.format(parser_prompt)

        # Template so we can inject previous_response
        prompt_template = PromptTemplate(json_prompt)
        self.output_pipeline = QueryPipeline(chain=[prompt_template, self.llm])

    def _create_json(self, query: str) -> dict:
        """Use the defined agent and pipeline, take user query and transform it
        to code and code metadata."""
        response = self.agent.query(query)
        next_response = self.output_pipeline.run(previous_response=response)
        cleaned_json = ast.literal_eval(
            str(next_response).replace("assistant:", "")
        )
        return cleaned_json

    # Applying retry decorator to create_json
    _create_json = retry(_create_json)

    @staticmethod
    def _save_code(cleaned_json: dict):
        """Use the created code metadata object and save a .py file.

        Args:
            cleaned_json (dict): Dictionary with keys defined by
                the CodeOutput class
        """
        filename = cleaned_json["filename"]
        try:
            with open(os.path.join("output", filename), "w") as f:
                f.write(cleaned_json["code"])
            print("Saved file", filename)
        except:
            print("Error saving file...")

    def execute(self):
        """Main function. This executes the whole workflow."""
        self._create_pdf_api_tool()
        self._define_tools()
        self._create_code_agent_from_tools()
        self._create_query_pipeline_gen_code()

        # example_prompt = "Read the contents of /llamaindex-project/data/AI-Agent-Code-Generator/test.py and write a python script that calls the post endpoint to make a new item"
        while (prompt := input("Enter a prompt (q to quit): ")) != "q":
            cleaned_json = self._create_json(prompt)
            self._save_code(cleaned_json)


if __name__ == "__main__":
    GenerateCodeFromQuery(
        "https://github.com/techwithtim/AI-Agent-Code-Generator",
        "AI-Agent-Code-Generator",
        "data",
    ).execute()
