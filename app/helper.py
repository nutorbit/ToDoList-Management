import dill
import pickle
import pandas as pd

from sklearn.externals import joblib
from pythainlp import word_tokenize

model = joblib.load('./models/01_model.pkl')
vectorizer = pickle.load(open('./models/01_vectorizer.pkl', 'rb'))


def getIntent(text):
    # tokenize text
    text = ' '.join(word_tokenize(text))

    # vectorize text
    text_feature = vectorizer.transform([text]).todense()
    df_text_feature = pd.DataFrame(text_feature,
                                   columns=list(map(lambda x: f'text_{x}', range(text_feature.shape[1]))))

    pred = model.predict(df_text_feature)

    return pred[0]
