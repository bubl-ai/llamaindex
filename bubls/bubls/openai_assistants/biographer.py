import openai as oa


class biographer:
    def __init__(
        self, person_info: str, first_degree_relatives_info: str = None
    ):
        self.person_info = person_info
        self.first_degree_relatives_info = first_degree_relatives_info
        self.cl = oa.OpenAI()

    def generate_biography(self):
        stream = self.cl.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are writing the biography of a member using information of the individual and about its relatives. Share as much detail as possible about their profession, family and life in general.",
                },
                {
                    "role": "assistant",
                    "content": f"This is the information of the individual you are writing the biography about. {self.person_info}",
                },
                {
                    "role": "assistant",
                    "content": f"This is the information of the first degree relatives {self.first_degree_relatives_info}",
                },
                {
                    "role": "user",
                    "content": "Write a biography with at least 4000 tokens using the information provided about the individual and their first degree relatives",
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
