import openai

def chat_gpt(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


class AnswerSetGenerator:
    MODEL_SET = {
        "chat-gpt": chat_gpt
    }

    PROMPT = """
        Synonym Generation Task

        The goal is to generate synonyms or label sets for a given word or phrase, the synonyms should be related to the domain and word/phrase itself

        Return output with a single JSON format with `word`:`synonym` key values

        Given the following domain provide the synonyms for the following word/phrase, and N is the number of synonyms to output
        ```
        Domain: {}
        Word: {}
        N: {}
        ```
    """
    def __init__(self, model:str ="chat-gpt"):
        self.model = self.MODEL_SET[model]

    def generate(self, label:str, domain:str, answer_set_no:int = 10):
        prompt = self.PROMPT.format(domain, label, answer_set_no)
        return self.model(prompt=prompt)

