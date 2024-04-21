import logging
import os
from typing import Any, Dict, List

import spotipy
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from spotipy.oauth2 import SpotifyClientCredentials

from dj_gpt.base_chain import BaseChain


class KeyWordResponse(BaseModel):
    keywords: list[str] = Field(..., description="The extracted keywords from the input text.")


class SongFinder(BaseChain):
    """Finds songs based on keyword extraction from user input using LangChain."""

    def __init__(self, verbose: bool = False) -> None:
        """Initializes with Spotify and LangChain configurations."""
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

        prompt = PromptTemplate.from_template(
            template="You are a music expert. Based on the following text, "
            "extract keywords with which one can search for songs on "
            "any major streaming-platform. The text is enclosed with tripple backticks.\n"
            "Respond in json format only with the following key and value pairs:\n"
            "- keywords, which is a list of strings containing the keywords. "
            "If none could be found return an empty list.\n\n"
            "Only extract keywords based on the given text. "
            "Do not include arbitrary keywords like song or artist aswell as actual artist names.\n\n"
            "```text\n{text}```",
        )

        super().__init__(prompt=prompt, pydantic_model=KeyWordResponse)
        if verbose:
            self._chain.verbose = True

    def extract_keywords(self, text: str) -> List[str]:
        """Extracts keywords from text using a GPT-powered prompt."""
        self.logger.debug(f"Extracting keywords for text: {text}")
        input = {"text": text}
        results = self.chain.invoke(input=input)["text"].get("keywords", [])
        self.logger.debug(f"Extracted: {results}")
        return results

    def search_songs(self, text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for songs on Spotify based on extracted keywords.

        Args:
                text (str): The input text to extract keywords from.
                top_k (int, optional): The number of songs to return. Defaults to 5.

        Returns:
                List[Dict[str, Any]]: A list of songs with the track and artist name.
        """
        keywords = self.extract_keywords(text)
        self.logger.debug(f"Searching for songs based on keywords: '{keywords}'")
        results = self.sp.search(q=" ".join(keywords), limit=top_k, type="track")
        tracks = results["tracks"]["items"]
        song_list = []
        for track in tracks:
            song_list.append({"track": track["name"], "artist": track["artists"][0]["name"]})
        self.logger.debug(f"Found {len(tracks)} songs.")
        return song_list
