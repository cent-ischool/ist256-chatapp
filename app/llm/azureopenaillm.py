from loguru import logger

from openai import AzureOpenAI
if __name__=='__main__':
    from llmbase import LLMBase
else:
    from .llmbase import LLMBase
    
from typing import List, Dict

class AzureOpenAILLM(LLMBase):

    def __init__(
            self, 
            endpoint: str, 
            api_key:str, 
            api_version: str,
            model: str, 
            temperature: float
        ):
        self.__endpoint = endpoint
        self.__api_version = api_version
        self._model = model
        self._temperature = temperature
        self._client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)
        logger.info(f"endpoint={self.__endpoint}, apiver={self.__api_version}, model={model}, temperature={temperature}")

    @property
    def model(self):
        return self._model
    
    @property
    def temperature(self):
        return self._temperature

    def generate_stream(self, messages: List[Dict], model: str|None=None,  temperature: float|None=None):
        this_model = model if model != None else self._model
        this_temperature = temperature if temperature != None else self._temperature
        logger.info(f"endpoint={self.__endpoint}, apiver={self.__api_version}, model={this_model}, temperature={this_temperature}")
        response = self._client.chat.completions.create(
            stream=True,
            model=this_model,
            messages=messages,
            temperature=this_temperature
        )
        
        for chunk in response:
            if len(chunk.choices) > 0:
                yield chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""

    def generate_text(self, messages: List[Dict], model: str|None=None,  temperature: float|None=None):
        this_model = model if model != None else self._model
        this_temperature = temperature if temperature != None else self._temperature
        logger.info(f"endpoint={self.__endpoint}, apiver={self.__api_version}, model={this_model}, temperature={this_temperature}")
        response = self._client.chat.completions.create(
            model=this_model,
            messages=messages,
            temperature=this_temperature
        )
        content = response.choices[0].message.content
        return content
    

if __name__=='__main__':
    import os
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.environ["AZURE_OPENAI_API_VERSION"]
    model = "gpt-4o-mini"
    temperature = 0.1
    llm = AzureOpenAILLM(endpoint, api_key, api_version, model, temperature)
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

    for chunk in llm.generate_stream(messages, temperature=llm.temperature+ 0.5):
        print(chunk)