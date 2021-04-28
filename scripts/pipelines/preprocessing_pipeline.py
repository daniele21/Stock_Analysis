from typing import Text

from keras_preprocessing.sequence import pad_sequences
from tensorflow.python.keras.utils.np_utils import to_categorical

from constants.config import MAX_WORD_SENTENCE
from core.preprocessing.imbalance import smote_oversampling
from core.preprocessing.tokenizers import CustomTokenizer
from scripts.data.extraction import extract_dataset
from scripts.data.preprocessing import tdidf_preprocessing, data_preprocessing
import numpy as np


def preprocessing_oversampling_tdidf(data_path: Text,
                                     preprocessing_text: bool = False):

    data = extract_dataset(data_path)

    if preprocessing_text:
        data = data_preprocessing(data)

    x, y = data['Phrase'], data['Sentiment']

    x_tdidf, tdidf = tdidf_preprocessing(x,
                                         n_gram_range=(1, 3),
                                         max_features=100)

    x_smote, y_smote = smote_oversampling(x_tdidf.toarray(),
                                          y,
                                          random_state=2021)

    return x_smote, y_smote
