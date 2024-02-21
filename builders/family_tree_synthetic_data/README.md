Example gotten from [llamaindex documentation](https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html)

How to use:
```
python williams_family.py
```

In any AI project, it's crucial to ensure a proper evaluation, clearly define a problem, and continually assess how well your solution addresses it. Regular evaluations and feedback loops are crucial for optimizing its performance, making the selection of data for building and evaluating your product a pivotal consideration.

In my case, I aimed for a simple dataset to explore various ideas and measure their impact on overall performance. Without a direct equivalent to MNIST for RAGs, I decided to create my own dataset using family tree information, perhaps influenced by binge-watching "The Crown" in the last few weeks. This dataset could effectively evaluate RAGs due to its interconnected documents and complex family tree structures, providing a good benchmark into different RAG configurations' performance.

It is known that RAGs excel at answering questions found directly in the indexed documents but struggle with meta-level questions. Therefore, my plan is to compare their performance on simple queries like "Who is person X" versus more complex ones like "How many cousins does person X have?"

Now, let me explain how I created this dataset. I first defined two classes, [Person and Family](https://github.com/bubl-ai/llamaindex-project/blob/main/bubls/bubls/synthetic_data/family_tree.py). 

- **Person**: Contains relevant information such as name, birthday, first-degree relatives, and life status. This class facilitates information organization and retrieval.

- **Family**: A collection of Persons forming a family tree. This class allows retrieving information about an individual and their immediate relatives.

I developed code that integrates these classes and initializes a fictional family, [The Williams](https://github.com/bubl-ai/llamaindex-project/blob/main/builders/family_tree_synthetic_data/williams_family.py). To create the dataset, I designed two "GPT assistants": a [Biographer](https://github.com/bubl-ai/llamaindex-project/blob/main/bubls/bubls/openai_assistants/biographer.py) and a [QA Generator](https://github.com/bubl-ai/llamaindex-project/blob/main/bubls/bubls/openai_assistants/qa_generator.py). The Biographer generates biographies based on the individual and its relatives information, and the QA Generator creates question-answer pairs about each biography. The dataset is available on our [Hugging Face profile](https://huggingface.co/datasets/bubl-ai/williams_family_tree).

The dataset is organized into two folders:

- **Biographies**: Contains narratives intricately woven based on our predefined family structure.

- **Test Questions**: Curates pairs of questions and answers derived from the biographies, serving as a valuable test dataset for evaluating various Retrieval-Augmented Generative (RAG) configurations.

Without delay, let's dive into the experimentation phase. Here, we'll test various RAG customizations and configurations, assessing their performances to gain insights into their strengths and weaknesses.
