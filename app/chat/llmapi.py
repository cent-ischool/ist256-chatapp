from llm.llmbase import LLMBase

class LLMAPI:
    def __init__(
            self, 
            llm: LLMBase, 
            model: str|None=None, 
            temperature: str|None=None, 
            system_prompt: str|None=None
        ):
        self._llm = llm
        self._model = model if model != None else llm.model
        self._temperature = temperature if temperature != None else llm.temperature
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

    def clear_history(self):
        # just system prompt 
        self._messages = [ self._messages[0] ]         

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

        response = self._llm.generate_stream(
            messages=messages,
            model=self._model,
            temperature=self._temperature
        )
        for chunk in response:
            yield chunk 
          

if __name__ == '__main__':
    import os
    from llm.ollamallm import OllamaLLM
    from llm.azureopenaillm import AzureOpenAILLM
    allm = AzureOpenAILLM(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        model="gpt-4o-mini",
        temperature=0.6
    )
    ollm = OllamaLLM(
        host_url=os.environ["OLLAMA_HOST"],
        model="dolphin3",
        temperature=0.3
    )
    llmapi1 = LLMAPI(llm=ollm, model="llama3", temperature=0.7, system_prompt="you only know about photosynthesis. only answer questions about photosynthesis")
    response1 = llmapi1.stream_response("explain photosynthesis like I'm a 5 year old?")
    assemble = ""
    for chunk in response1:
        assemble += chunk
    print(assemble)
    response1 = llmapi1.stream_response("explain photosynthesis like I'm a 10 year old?")
    assemble = ""
    for chunk in response1:
        assemble += chunk
    print(assemble)
    response1 = llmapi1.stream_response("what is the capital of France?")
    assemble = ""
    for chunk in response1:
        assemble += chunk
    print(assemble)
    llmapi1.clear_history()
    response1 = llmapi1.stream_response("what is the last thing I asked you?")
    assemble = ""
    for chunk in response1:
        assemble += chunk
    print(assemble)
    print("========================================")
    llmapi2 = LLMAPI(llm=allm)
    response2 = llmapi2.stream_response("explain photosynthesis like I'm a 5 year old?")
    assemble = ""
    for chunk in response2:
        assemble += chunk
    print(assemble)
