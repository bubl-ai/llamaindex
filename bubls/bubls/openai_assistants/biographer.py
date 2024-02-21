import openai as oa

SYSTEM_CONTENT = (
    "You are writing the biography of a member using information of the "
    "individual and about its relatives. Share as much detail as possible "
    "about their profession, family and life in general."
)

USER_CONTENT = (
    "Write a biography with at least 4000 tokens using the information "
    "provided about the individual and their first degree relatives"
)


class Biographer:
    def __init__(
        self, person_info: str, first_degree_relatives_info: str = None
    ):
        """Initialize an assistant that generates the biography of a person using
        the information provided. The biography is mainly focused on the family
        tree structure of the individual.

        Args:
            person_info (str): Information of the individual the biography is
                written about.
            first_degree_relatives_info (str, optional): Information about all
                the first degree relatives. Defaults to None.
        """
        self.person_info = person_info
        self.first_degree_relatives_info = first_degree_relatives_info
        self.openai_client = oa.OpenAI()

    def generate_biography(self) -> str:
        """Use openai client to generate a biography.

        Returns:
            str: biography
        """
        stream = self.openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_CONTENT},
                {
                    "role": "assistant",
                    "content": f"This is the information of the individual you are writing the biography about. {self.person_info}",
                },
                {
                    "role": "assistant",
                    "content": f"This is the information of the first degree relatives {self.first_degree_relatives_info}",
                },
                {"role": "user", "content": USER_CONTENT},
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
