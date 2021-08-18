# Файл создания датасета для обучения модели №3


import os
from pandas import DataFrame
from text_extracting import to_text

names_of_images = os.listdir('C:\\Users\\hom1c1d3\\PycharmProjects\\directum\\source')
text_dict = {}
df = DataFrame(columns=['name', 'text', 'first'])
index = 0
for i in names_of_images:
    text = to_text(f'C:\\Users\\hom1c1d3\\PycharmProjects\\directum\\source\\{i}')
    if i[-6:-4] == '_1' or '_' not in i:
        first = 1
    else:
        first = 0
    df.loc[index] = [i, text, first]
    print(df.loc[index])
    index += 1
print(df)
df.to_csv('new.csv', index=False)