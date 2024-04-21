from abc import ABC
from typing import Optional

from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI


class BaseChain(ABC):
    def __init__(self, prompt: PromptTemplate, llm_chain: Optional[LLMChain] = None, pydantic_model: Optional = None):
        """
        Initializes the BaseChain with a language model chain.

        If no language model chain is provided, a new one is created using the provided model name, prompt, and output parser.

        Args:
            prompt (PromptTemplate): The prompt template to use with the language model chain.
            llm_chain (LLMChain, optional): An existing language model chain. Defaults to None.
            pydantic_model (optional): The Pydantic model to use with the output parser. Defaults to None.
        """
        self.__model_name = "gpt-3.5-turbo-instruct"
        self.__prompt = prompt
        self.__pydantic_model = pydantic_model
        if llm_chain is None:
            llm = OpenAI(model_name=self.__model_name, temperature=0)
            if self.__pydantic_model is not None:
                self._chain = LLMChain(
                    prompt=prompt, llm=llm, output_parser=JsonOutputParser(pydantic_model=self.__pydantic_model)
                )
            else:
                self._chain = LLMChain(
                    prompt=prompt,
                    llm=llm,
                )
        else:
            self._chain = llm_chain
            self._prompt = self._chain.prompt
            self.__output_parser = self._chain.output_parser

    @property
    def chain(self):
        """
        Gets the language model chain.

        Returns:
            LLMChain: The language model chain.
        """
        return self._chain

    @property
    def prompt(self):
        """
        Gets the prompt template used by the language model chain.

        Returns:
            PromptTemplate: The prompt template.
        """
        return self.__prompt

    @prompt.setter
    def prompt(self, value):
        """
        Sets the prompt template for the language model chain.

        Args:
            value (PromptTemplate): The new prompt template.
        """
        self.__prompt = value

    @property
    def model_name(self):
        """
        Gets the name of the language model.

        Returns:
            str: The name of the language model.
        """
        return self.__model_name

    @model_name.setter
    def model_name(self, value):
        """
        Sets the name of the language model and re-initializes the language model chain with the new model name.

        Args:
            value (str): The new name of the language model.
        """
        self.__model_name = value
        self._chain = LLMChain(
            llm=OpenAI(model_name=self.__model_name), prompt=self._chain.prompt, output_parser=self._chain.output_parser
        )
