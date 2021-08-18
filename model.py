import pickle


def predict(text):  # Предсказание класса для классификации страниц (задание №3)
    model = pickle.load(open('gpr_model.sav', 'rb'))  # Подгрузка
    pred = model.predict([text])
    return pred
