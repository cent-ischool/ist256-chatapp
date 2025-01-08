from ollama import Client
from constants import TEMPERATURE


class OllamaAPI:
    def __init__(self, ollama_host, model="llama3", system_prompt=None):
        self._client = Client(
            host=ollama_host
        )
        self._model = model
        self._messages = [
            {
                "role": "system", 
                "content": "You are a helpful AI assistant." if system_prompt == None else system_prompt 
            }
        ]

    def _add_to_messages(self, role, content):
        self._messages.append(
            {
              "role": role,
              "content": content
            }
        )

    @property
    def history(self):
        return self._messages
    
    @property
    def system_prompt(self):
        return [m for m in self._messages if m['role'] == "system"]

    @system_prompt.setter
    def system_prompt(self, value):
        index = [i for i, m in enumerate(self._messages) if m['role'] == "system"][0]
        self._messages[index]['content'] = value

    def record_response(self, assistant_reponse):
        self._add_to_messages("assistant", assistant_reponse)

    def stream_response(self, user_query, ignore_history=False):
        self._add_to_messages("user", user_query)
        if not ignore_history:
            messages = self._messages
        else:
            messages = self.system_prompt + [{"role": "user", "content": user_query}]

        response = self._client.chat(
            stream=True,
            model=self._model,
            messages=messages,
            options={"temperature": TEMPERATURE} 
        )
        
        for chunk in response:
            content = chunk['message']['content']
            yield content

          

if __name__ == '__main__':
    import os
    client = OllamaAPI(
        ollama_host=os.environ.get("OLLAMA_HOST","https://ollama-proxy.cent-su.org"),
        model="llama3",
        system_prompt="You are a helpful AI assistant that speaks like a pirate."
    )
    models = client._client.list()
    print(models)
    # response = client.stream_response("Why is the sky blue?")
    # for chunk in response:
    #     print(chunk, end='', flush=True)