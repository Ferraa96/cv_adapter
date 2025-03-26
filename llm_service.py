from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class LLMService:
    
    def __init__(self, provider: str, api_key: str, model_name: str=None):
        self.llm = self.get_llm(provider, api_key, model_name)
        self.provider_name = provider
        self.model_name = model_name
        
    
    def get_llm(self, provider: str, api_key: str, model_name: str=None):
        """
        Get the LLM model based on the provider.
        
        Args:
        - provider (str): The provider to use for the LLM model.
        - api_key (str): The API key to use for the LLM model.
        - model_name (str): The name of the model to use for the LLM model.
        
        Returns:
        - LLM: The LLM model based on the provider.
        """
        match provider:
            case "ollama":
                llm = OllamaLLM(model=model_name)
            case "openai":
                llm = ChatOpenAI(temperature=0, model="gpt-4o", api_key=api_key)
            case "groq":
                llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=api_key)
            case _:
                raise ValueError("Invalid provider. Supported providers are 'ollama', 'openai', and 'groq'.")
        
        return llm
    
    
    def get_text_result(self, result):
        match self.provider_name:
            case 'ollama':
                return result
            case 'openai':
                return result.choices[0].text
            case 'groq':
                return result.content
    
    
    def query_llm(self, prompt: str, variables: dict[str, str]):
        """
        Query the LLM model with the given prompt and variables.
        
        Args:
        - prompt (str): The prompt to query the LLM model with.
        - variables (dict): The variables to use in the prompt.
        
        Returns:
        - str: The result of the query.
        """
        prompt = PromptTemplate(
            input_variables=list(variables.keys()),
            template=prompt
        )
        
        chain = prompt | self.llm
        result = chain.invoke(variables)
        
        return self.get_text_result(result)