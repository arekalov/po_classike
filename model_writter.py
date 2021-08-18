# Файл создания модели для классификации страниц (№ 3)

from lightgbm import LGBMClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

df = read_csv('new.csv')
X_train, X_test, y_train, y_test = train_test_split(df.drop('first', axis=1), df['first'], test_size=0.2)
print()
pipe = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('csf', LGBMClassifier())])
pipe.fit(X_train['text'], y_train)
pred = pipe.predict(X_test['text'])
print(accuracy_score(y_train, pipe.predict(X_train.text)))
print(accuracy_score(y_test, pred))

import pickle

# Сохранение модели в .sav
filename = 'gpr_model.sav'
pickle.dump(pipe, open(filename, 'wb'))
