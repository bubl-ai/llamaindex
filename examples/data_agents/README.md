LlamaIndex offers a toolkit that enables the establishment of a query interface around data for various tasks using LLMs. One of these functionalities allows for the creation of a Data Agent chatbot powered by LLMs, capable of intelligently executing tasks over your data.

These examples were was inspired by the tutorial series on Agents and Tools provided by LlamaIndex in their April 16, 2024, newsletter. Additionally, they have shared tutorial series videos available [here](https://www.youtube.com/watch?v=-AuHlVMyEA0).

These examples offer valuable insights for anyone interested in gaining a deeper understanding of agent reasoning to develop simple applications.

## What are Data Agents
Data Agents expand upon the capabilities of traditional query engines by enabling continuous interaction with data sources, providing a more adaptable and responsive approach to data management. Their ability to intelligently execute tasks over data allows for autonomous searches, retrieval, and ingestion of new information, with the capability to adapt based on this data. Additionally, they can integrate with external service APIs and perform operations such as reading, modifying, and writing data.

The main core steps of a Data Agent include:
- **Reasoning Loop:** This loop determines how the Agent will interact with different data tools. LlamaIndex supports a [variety of Agents and functionalities](https://docs.llamaindex.ai/en/stable/examples/agent/Chatbot_SEC/), including:
   - [**ReAct Agent:**](https://docs.llamaindex.ai/en/stable/examples/Agent/react_Agent_with_query_engine/) It involves a 3-step process: Thought (determine which tool to use), Action (use the tool to take an action), and Observation (check the result and iterate until a final result is obtained).
   - [**Function Calling Agent:**](https://docs.llamaindex.ai/en/stable/examples/Agent/openai_Agent_parallel_function_calling/) A unified abstraction that utilizes function calling capabilities of different LLMs to call given tools.
   - [**Chain-of-Abstraction Agent:**](https://docs.llamaindex.ai/en/stable/examples/agent/coa_agent/) Implements a generalized version of the strategy described in the [original paper](https://arxiv.org/pdf/2401.17464.pdf). It enables LLMs to learn more general reasoning strategies that are robust to shifts of domain knowledge relevant to different reasoning questions.
   - [**Retrieval Augmented:**](https://docs.llamaindex.ai/en/stable/examples/Agent/openai_Agent_retrieval/) Utilizes an Agent together with a tool retriever to manage an index on an arbitrary number of data tools, reducing latency and cost by retrieving only relevant tools.
   - [**Controlling Reasoning Loop:**](https://docs.llamaindex.ai/en/stable/examples/Agent/return_direct_Agent/?h=return_direct) Allows modification of the Agent reasoning loop, where the output is returned directly instead of using an LLM, useful for speeding up response times.
   - [**Step-wise Controllable:**](https://docs.llamaindex.ai/en/stable/examples/agent/agent_runner/agent_runner/) Provides more granular control of the Agent by separating task creation and execution, enabling sharing feedback to the Agent as it completes tasks.

- **Tool Abstractions:** Based on the decision-making process in the Reasoning Loop, the Agent selects the most relevant tools to fetch or modify data. Tool abstractions provide a structured way to define how Data Agents interact with data or services Types of Tools include:
   - **FunctionTool:** Converts user-defined functions into Tools and auto-infers function schemas.
   - **QueryEngineTool:** Wraps existing query engines. 
   - [**Llama Hub Tools:**](https://llamahub.ai/?tab=tools) Utilities allowing large language models to read from and write to third-party data services and sources.
