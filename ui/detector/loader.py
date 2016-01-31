import nltk
import json
import numpy as np
from random import shuffle

# Define languages to pull in
def loaderShuffleData():
    #langs = ('User_ru-N.json','User_en-us-N.json','User_de-N.json', 'User_yue-N.json','User_fr-N.json')

    langs = ('User_fr-N.json','User_en-N.json', 'User_ru-N.json')
    dataset = []

    # Pull data into array as tuples of each string and the language
    for l in langs:
        language=l[5:7]
        json_data = open('jsons/'+l).read()
        data = json.loads(json_data)
        for entry in data:
            dataset.append((entry["text"], language))

    #Shuffle up the data!
    shuffle(dataset)

    # for i in range(0, 6):
    #     print(dataset[i])

    # Split data into train and test
    size = dataset.__len__()

    trainsize = 0.8

    train = dataset[0:int(np.ceil(trainsize*size))]
    test = dataset[int(np.ceil(trainsize*size)):]
    return train

def loaderShuffleDataTest():
    #langs = ('User_ru-N.json','User_en-us-N.json','User_de-N.json', 'User_yue-N.json','User_fr-N.json')
    langs = ('User_en-N.json','User_fr-N.json','User_ru-N.json')
    dataset = []

    # Pull data into array as tuples of each string and the language
    for l in langs:
        language=l[5:7]
        json_data = open('jsons/'+l).read()
        data = json.loads(json_data)
        for entry in data:
            dataset.append((entry["text"], language))

    #Shuffle up the data!
    shuffle(dataset)

    # for i in range(0, 6):
    #     print(dataset[i])

    # Split data into train and test
    size = dataset.__len__()

    trainsize = 0.8

    train = dataset[0:int(np.ceil(trainsize*size))]
    test = dataset[int(np.ceil(trainsize*size)):]
    return test

#def TrainTestSplit(dataset, trainsize):
#    # Split data into train and test
#    size = dataset.__len__()
#
#    dataset = shuffle(dataset)
#    train = dataset[0:int(np.ceil(trainsize*size))]
#    test = dataset[int(np.ceil(trainsize*size)):]
#
#    return word2vec.load("word2vec_model.bin")
#
#example = train[0]
#print example[0].__len__()


def GetWordVecRepresentation(example, embeddings, oov_rescale=0.01):

    # Set up input vector
    input_vec = []

    # Iterate through tokens and get word vec representations
    for i in example[0]:
        if i in embeddings:
            input_vec.append(embeddings[i])
        else:
            input_vec.append(np.random.randn(1,10) * oov_rescale)

    return input_vec