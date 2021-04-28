from typing import Text, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from core.preprocessing.text_preprocessing import remove_punctuations, stem_sentence, lemmatize_sentence, \
    remove_stopwords, init_nltk
import logging

from core.preprocessing.tokenizers import MyTokenizer
from core.utils.time_utils import timestamp

logger = logging.getLogger(__name__)


def data_preprocessing(data: pd.DataFrame,
                       punctuations: bool = True,
                       lowering: bool = True,
                       stemming: bool = False,
                       lemmatization: bool = True,
                       stop_words: bool = True,
                       save_dir: Text = None):

    prep_data = data.copy(deep=True)
    logger.info('> Data Preprocessing')

    init_nltk()

    if punctuations:
        logger.info('\t> Removing Punctuations')
        prep_data['Phrase'] = prep_data['Phrase'].apply(remove_punctuations)

    if lowering:
        logger.info('\t> Lowering')
        prep_data['Phrase'] = prep_data['Phrase'].apply(lambda x: str(x).lower())

    if stop_words:
        logger.info('\t> Removing Stop Words')
        prep_data['Phrase'] = prep_data['Phrase'].apply(remove_stopwords)

    if stemming:
        logger.info('\t> Stemming')
        prep_data['Phrase'] = prep_data['Phrase'].apply(stem_sentence)

    if lemmatization:
        logger.info('\t> Lemmatization')
        prep_data['Phrase'] = prep_data['Phrase'].apply(lemmatize_sentence)

    prep_data = prep_data.dropna()

    if save_dir:
        filename = f'prep_data_{timestamp()}'
        filepath = f'{save_dir}{filename}.csv'
        prep_data.to_csv(filepath)
        logger.info(f'Preprocessed Data saved at {filepath}')

    return prep_data


def tdidf_preprocessing(x,
                        n_gram_range: Tuple = (1, 3),
                        max_features: int = 10000):

    tdidf = TfidfVectorizer(ngram_range=n_gram_range,
                            max_features=max_features)

    tdidf.fit(x)

    x_tdidf = tdidf.transform(x)

    return x_tdidf, tdidf





