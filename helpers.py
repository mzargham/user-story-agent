import requests
from os import environ
from dataclasses import dataclass

class Llm:
    def __init__(self, model_identifier: str = "gpt-4-1106-preview", 
                 url: str = "https://api.openai.com/v1/chat/completions", 
                 role: str = "user",
                 auth: dict = {"Authorization": f"Bearer {environ.get('OPENAI_API_KEY')}"}):
        
        self.model_identifier = model_identifier
        self.url = url
        self.role = role
        self.auth = auth

    #add setters and getters for the above attributes
    # Getter for model_identifier
    @property
    def model_identifier(self):
        return self._model_identifier

    # Setter for model_identifier
    @model_identifier.setter
    def model_identifier(self, value):
        self._model_identifier = value

    # Getter for url
    @property
    def url(self):
        return self._url

    # Setter for url
    @url.setter
    def url(self, value):
        self._url = value

    # Getter for role
    @property
    def role(self):
        return self._role

    # Setter for role
    @role.setter
    def role(self, value):
        self._role = value

    # Getter for auth
    @property
    def auth(self):
        return self._auth

    # Setter for auth
    @auth.setter
    def auth(self, value):
        self._auth = value
        
    def prompt(self, text: str) -> str:
        # Method to send a prompt to the LLM and return its response
        url = self.url
        req = {
            "model": self.model_identifier,
            "messages":[
                {"role": self.role, "content": text}
            ]
        }
        #print(req)
        response = requests.post(url, json=req, headers=self.auth)  # Use json parameter to send the request payload as JSON
        raw =  response.json()
        try:
            return f"{response.json()['choices'][0]['message']['content']}"
        except:
            return raw
        
        def prompt_with_context(self, text: str, context: str) -> str:
            # method takes in a prompt and a context, appends the contexts before the prompt, then prompts and returns the response
            prompt = f"{context}\n{text}"
            return self.prompt(prompt)

@dataclass
class Agent:
    name: str
    llm: Llm
    context: str
    user_story: str

    def observe(self, text: str) -> None:
        # method takes in a string and appends it to the agent's context
        self.context = f"{self.context}\n{text}"

    def cogitate(self) -> str:
        text = "Reflect on your experiences and describe your learnings."
        return self.prompt(f"{self.user_story}\n{text}")

    # not that prompting an agent includes that agebt's context and it remembers the interaction
    def prompt(self, text: str) -> str:
        # method takes in a prompt and appends the agent's context before the prompt, then prompts and returns the response
        prompt = f"{self.context}\n{self.user_story}\n{text}"
        response = self.llm.prompt(prompt)
        self.observe(f"{text}\n{response}")
        return response
    