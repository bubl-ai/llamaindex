import openai as oa

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
        self.cl = oa.OpenAI()

    def generate_qa(self) -> str:
        """Use openai client to generate the QA.

        Returns:
            str: QA in csv format
        """
        stream = self.cl.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_CONTENT},
                {
                    "role": "assistant",
                    "content": f"This is the input text {self.input_text}",
                },
                {
                    "role": "user",
                    "content": f"Generate a total of {self.number_of_questions} questions and answers",
                },
            ],
            stream=True,
            top_p=0.9,
            model="gpt-3.5-turbo",
        )

        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content

        return response
