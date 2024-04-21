import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dj_gpt.base_chain import BaseChain


class Summarizer(BaseChain):
    """Generates text using OpenAI models based on input data.

    Attributes:
        logger (logging.Logger): a logger instance used for logging events during the execution
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initializes the text generator with an API key from environment variables.

        Args:
            verbose (bool, optional): a flag used to set the logging level (default is False, which sets the logging level to WARNING)
        """
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

        prompt = PromptTemplate.from_template(
            "You are an expert in summarizing multiple texts into one. Based on the following texts, "
            "generate a short summary that captures the essence of the input. "
            "The texts are enclosed with tripple backticks. Each individual text is separated by ---\n\n"
            "```text\n{text}```"
        )
        super().__init__(prompt=prompt)
        if verbose:
            self._chain.verbose = True

    def summarize(self, texts: list[str]) -> str:
        """Generates a text description based on the data provided.

        Args:
            texts (list[str]): a list of texts to be summarized

        Returns:
            str: a string that represents the summary of the provided texts
        """
        concatenated_text = "\n---\n".join(texts)
        chunks = self._split_text(text=concatenated_text)
        inputs = [{"text": chunk} for chunk in chunks]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.chain.invoke, input) for input in inputs]
            results = [future.result() for future in as_completed(futures)]
        description = "\n".join([result["text"] for result in results])
        return description.strip()

    def _split_text(self, text: str, chunk_size: int = 3900, chunk_overlap: int = 100) -> list[str]:
        """Split a text into chunks of a specific max token size with an overlap between each chunk.
        The overlap is to ensure that the model can generate coherent text across chunks and nothing is cut off.

        Args:
            text (str): The text to split
            chunk_size (int, optional): The size of each chunk. Defaults to 4096.
            chunk_overlap (int, optional): The overlap between each chunk. Defaults to 100.

        Returns:
            list[str]: A list of text chunks
        """
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-3.5-turbo-instruct", chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return splitter.split_text(text)
