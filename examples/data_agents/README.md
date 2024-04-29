These examples offer valuable insights for anyone interested in gaining a deeper understanding of Agent reasoning to develop simple applications:

## What are Data Agents
Query Engines are very powerful for reading capabilities, but they miss the opportunity to enable a rich set of interactions with data. For example:
- General reasoning over any set of tools, whether from a database or an API.
- Both read and write capabilities, they should be able to do more than search and retrieval from a static knowledge source.

This is the context where Data Agents originated. They expand upon the capabilities of traditional query engines by enabling continuous interaction with data sources, providing a more adaptable and responsive approach to data management. Their ability to intelligently execute tasks over data allows for autonomous searches, retrieval, and ingestion of new information, with the capability to adapt based on this data. Additionally, they can integrate with external service APIs and perform operations such as reading, modifying, and writing data. As said by LLamaIndex, Agents are a step beyond query engines in that they can not only "read" from a static source of data, but can dynamically ingest and modify data from a variety of different tools.

Data Agents are capable of performing both simple and complex data tasks because they can:
- Automate search and retrieval over different types of data.
- Call external service API in a structured fashion. 
- Process a response immediately, or index/cache it for future use.
- Store conversation history.

The main core steps of a Data Agent include:
- **Reasoning Loop:** Given an input task, the data Agent uses a reasoning loop to decide which tools to use, in which sequence, and the parameters to call each tool. In other words, this loop determines how the Agent will interact with different data tools. LlamaIndex supports a [variety of Agents and functionalities](https://docs.llamaindex.ai/en/stable/examples/agent/Chatbot_SEC/), including:
   - [**ReAct Agent:**](https://docs.llamaindex.ai/en/stable/examples/agent/react_agent_with_query_engine/) The ReAct Agent utilizes general text completion endpoints, enabling its use with any LLM. These text completion endpoints follow a simple input string to output string format, requiring the reasoning logic to be encoded in the prompt. It involves a 3-step process: Thought (determine which tool to use), Action (use the tool to take an action), and Observation (check the result and iterate until a final result is obtained).
   - [**Function Calling Agent:**](https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent_parallel_function_calling/) A unified abstraction that utilizes function calling capabilities of different LLMs to call given tools.
   - [**Chain-of-Abstraction Agent:**](https://docs.llamaindex.ai/en/stable/examples/agent/coa_agent/) Implements a generalized version of the strategy described in the [original paper](https://arxiv.org/pdf/2401.17464.pdf). It enables LLMs to learn more general reasoning strategies that are robust to shifts of domain knowledge relevant to different reasoning questions.
   - [**Retrieval Augmented:**](https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent_retrieval/) Utilizes an Agent together with a tool retriever to manage an index on an arbitrary number of data tools, reducing latency and cost by retrieving only relevant tools.
   - [**Controlling Reasoning Loop:**](https://docs.llamaindex.ai/en/stable/examples/agent/return_direct_agent/?h=return_direct) Allows modification of the Agent reasoning loop, where the output is returned directly instead of using an LLM, useful for speeding up response times. This also allows direct output returns, reducing costs and enhancing response efficiency.
   - [**Step-wise Controllable:**](https://docs.llamaindex.ai/en/stable/examples/agent/agent_runner/agent_runner/) Provides more granular control of the Agent by separating task creation and execution, enabling sharing feedback to the Agent as it completes tasks.

- **Tool Abstractions:** A data Agent is initialized with set of APIs that it interacts with and calls to return information or modify state. Based on the decision-making process in the Reasoning Loop, the Agent selects the most relevant tools to fetch or modify data. Tool abstractions provide a structured way to define how Data Agents interact with data or services. Defining a set of Tools is similar to defining API interfaces meant for Agent use. 
Types of Tools in LlamaIndex:
   - **FunctionTool:** A function tool allows users to easily convert any function into a Tool. Converts user-defined functions into Tools and auto-infers function schemas.
   - **QueryEngineTool:** Wraps over LlamaIndex query engines, providing a seamless transition to Agents. 
   - **Tool Specs:** This functionality enables users to define complete services, rather than just individual tools for performing isolated tasks. It entails a comprehensive API specification that an Agent can engage with, and a tool specification can be transformed into a roster of tools with which an Agent can be initialized. Each tool may engage with services through read/write endpoints.
   - [**Llama Hub Tool Repository:**](https://llamahub.ai/?tab=tools) ToolSpec utilities that define one or more tools around a single service, allowing LLMs to read from and write to third-party data services and sources. LlamaIndex provides a broad list of examples, you can find them [here](https://github.com/run-llama/llama-hub/tree/main/llama_hub/tools/notebooks).
   - **Utiltiy Tools:** When querying an API, it's common to receive a large volume of data, which may exceed the context window of the LLM. Utility Tools serve to wrap other tools and simplify the process of designing Agents to interface with various API services that produce substantial data. Examples include OnDemandLoaderTool and LoadAndSearchToolSpec.
