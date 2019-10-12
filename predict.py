from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
import os
import keras
import pandas as pd
import numpy as np
np.random.seed(1337)

model = load_model('./resources/model')
model._make_predict_function()
print("model loaded")
max_words = 1000
max_len = 150
X_train = pd.read_csv('./resources/X_train.csv',
                      header=None, index_col=0, squeeze=True)
X_test = pd.read_csv('./resources/X_test.csv',
                     header=None, index_col=0, squeeze=True)
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X_train)
sequences = tok.texts_to_sequences(X_train)
sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)


def predict(argv):
    series = pd.Series([argv])

    def modelPredict(predict, model):
        test_sequences = tok.texts_to_sequences(predict)
        test_sequences_matrix = sequence.pad_sequences(
            test_sequences, maxlen=max_len)
        return model.predict(test_sequences_matrix)
    modelPredict(series, model)
    return str(round(modelPredict(series, model).item(0)*100, 2))
