import spacy


def ner_predict(text): # Составление json файла для определения именованных сущностей (задание №4)
    nlp = spacy.load("en_core_web_sm")
    dict = {}
    doc2 = nlp(text)

    for ent in doc2.ents:
        if ent.label_ in dict.keys():
            dict[ent.label_].append(ent.text)
        else:
            dict[ent.label_] = [ent.text]
    new_dict = {}
    for key in dict.keys():
        if key == 'ORG':
            new_dict['ORGANIZATION'] = dict[key]
        elif key == 'GPE':
            new_dict['LOCATION'] = dict[key]
        elif key == 'DATE':
            new_dict['DATE'] = dict[key]
        elif key == 'MONEY':
            new_dict['MONEY'] = dict[key]
        elif key == 'PERSON':
            new_dict['PERSON'] = dict[key]
    json_final = []
    index = 0
    offset_counter = 0
    for key in new_dict.keys():
        for i in new_dict[key]:
            json_final.append({'text': i, 'tag': key, 'tokens': []})
            for j in i.split():
                json_final[index]['tokens'].append({'text': j, 'ofset': offset_counter})
                offset_counter += len(j)
            index += 1

    return ({'facts': json_final})
