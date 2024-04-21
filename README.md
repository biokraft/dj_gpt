# DJ-GPT

<p align="left">
  <img src="https://i.imgur.com/exyDRdG.png" width="120" height="120">
</p>

![Latest Version](https://img.shields.io/badge/version-0.1.0-g)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2C%203.10%2C%203.11-blue?logo=python)
[![Documentation](https://img.shields.io/badge/documentation-view-blue?logo=read-the-docs)](https://biokraft.github.io/dj_gpt/)
![Code Style Black](https://img.shields.io/badge/code%20style-black-black)
[![License](https://img.shields.io/badge/License-Apache%202.0-g.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI](https://img.shields.io/badge/PyPI-View%20on%20PyPI-blue?logo=pypi)](https://pypi.org/project/dj-gpt/)
[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-lightgrey?logo=github)](https://github.com/biokraft/dj_gpt)

DJ-GPT is an open-source Python application designed to integrate natural language processing with music discovery, utilizing Spotify's library and OpenAI's GPT models.
You can find the official documentation [here](https://biokraft.github.io/dj_gpt/).

# Installation

## Prerequisites

Ensure you have:
- Python 3.9 or newer installed.
- [Poetry](https://python-poetry.org/docs/) installed for dependency management.
- [Spotify Developer Account](https://developer.spotify.com/) to obtain API keys.
- [OpenAI Account](https://platform.openai.com/) to obtain API keys.

## Clone the Repository

```bash
git clone https://github.com/biokraft/dj_gpt.git
cd dj-gpt
```

## Install dependencies
```bash
poetry install
```

## Required API KEYS
### Spotify API Key
Sign up or log in at Spotify Developer Dashboard.
Create an app to obtain Client ID and Client Secret.

### Set environment variables:
```bash
export SPOTIFY_CLIENT_ID='your_client_id'
export SPOTIFY_CLIENT_SECRET='your_client_secret'
```

### OpenAI API Key
Obtain an API key by registering at OpenAI.
Set the API key as an environment variable:
```bash
export OPENAI_API_KEY='your_openai_api_key'
```

## Contributing
Contributions are welcome! Please fork the project and submit pull requests with your suggested changes.

## License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
