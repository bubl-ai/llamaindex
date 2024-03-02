from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

SYSTEM_CONTENT = (
    "You are an assistant that uses the input text to generate questions and "
    "answers. The output must be in the format of a csv file with two columns: question, answer"
)


class QAGenerator:
    def __init__(self, input_text: str, number_of_questions: int = 20):
        """Initialize an assistant that generates questions and answers
        in csv format for a given text. This is specially useful for testing
        the performance of a RAGs.

        Args:
            input_text (str): Text that will be used to create the QA from.
            number_of_questions (int, optional): How many QA tuples to create.
                Defaults to 20.
        """
        self.input_text = input_text
        self.number_of_questions = number_of_questions
        self.llm = OpenAI(model="gpt-3.5-turbo", top_p=0.9)

    def generate_qa(self) -> str:
        """Use openai client to generate the QA.

        Returns:
            str: QA in csv format
        """
        chat_history = [
            ChatMessage(role="system", content=SYSTEM_CONTENT),
            ChatMessage(
                role="assistant",
                content=f"This is the input text {self.input_text}",
            ),
            ChatMessage(
                role="user",
                content=f"Generate a total of {self.number_of_questions} questions and answers",
            ),
        ]

        response = self.llm.chat(chat_history)

        return response.message.content
