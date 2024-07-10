# SNAP-X

## Web and Social Network Search and Analysis

### Università di Milano-Bicocca

#### Authors

- Ventimiglia Michele - 502230
- Manuel Dellabona - XXXXXX

## Pre-trained Models

The pre-trained models used in this project were obtained from the following sources:

- **Sentiment Analysis Model:** `twitter-roberta-base-sentiment` from Hugging Face's `transformers` library.
- **NER Model:** `en_core_web_sm` from spaCy.

## Requirements

The following libraries and tools are required to run this project:

### Libraries

- `tqdm`
- `numpy`
- `scipy`
- `torch`
- `spacy`
- `pandas`
- `chardet`
- `networkx`
- `wordcloud`
- `matplotlib`
- `python-terrier`
- `transformers[sentencepiece]`

### Installation

You can install the required libraries using pip:
`pip install tqdm numpy scipy torch spacy pandas chardet networkx wordcloud matplotlib python-terrier transformers[sentencepiece]`

Additionally, you need to download the pre-trained models for spaCy and Hugging Face:
`python -m spacy download en_core_web_sm`
`python -m spacy download pt_core_news_sm`

### Dataset

[X (Twitter) Archive](https://archive.twitter-trending.com/italy/05-01-2023)
