from loguru import logger

from ollama import Client

if __name__=='__main__':
    from llmbase import LLMBase
else:
    from .llmbase import LLMBase

from typing import List, Dict


class OllamaLLM(LLMBase):

    def __init__(
            self, 
            host_url: str, 
            model: str, 
            temperature: float
        ):
        self.__host_url = host_url  
        self._model = model
        self._temperature = temperature
        self._client = Client(
            host=host_url
        )
        logger.info(f"host={self.__host_url}, model={model}, temperature={temperature}")

    @property
    def model(self):
        return self._model
    
    @property
    def temperature(self):
        return self._temperature        

    def generate_stream(self, messages: List[Dict], model: str|None=None,  temperature: float|None=None):
        this_model = model if model != None else self._model
        this_temperature = temperature if temperature != None else self._temperature
        logger.info(f"host={self.__host_url}, model={this_model}, temperature={this_temperature}")
        response = self._client.chat(
            stream=True,
            model=this_model,
            messages=messages,
            options={"temperature": this_temperature} 
        )
        
        for chunk in response:
            content = chunk['message']['content']
            yield content

    def generate_text(self, messages: List[Dict], model: str|None=None,  tempeature: float|None=None):
        this_model = model if model != None else self._model
        this_temperature = tempeature if tempeature != None else self._temperature
        logger.info(f"host={self.__host_url}, model={this_model}, temperature={this_temperature}")
        response = self._client.chat(
            model=this_model,
            messages=messages,
            options={"temperature": this_temperature} 
        )
        content = response['message']['content']
        return content 
          

if __name__=='__main__':
    import os
    ollama_host = os.environ["OLLAMA_HOST"]
    model = "llama3"
    temperature = 0.5
    stream = True
    llm = OllamaLLM(ollama_host, model, temperature)
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful AI assistant." 
        },
        {
            "role": "user", 
            "content": "What is the capital of New York?"
        }
    ]
    output = llm.generate_text(messages)
    print(output)

    for chunk in llm.generate_stream(messages, model="dolphin3", temperature=llm.temperature+ 0.3):
        print(chunk)