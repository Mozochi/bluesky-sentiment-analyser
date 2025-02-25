from .data_utils import *
from .naive_bayes import *

def train(model, data, labels):
    vocab = build_vocab(data)
    # print("Vocabulary:", vocab) For debugging purposes

    X_train = text_to_binary_vectors(data, vocab)
    # print("Training Vectors:", X_train) For debugging purposes

    model.fit(X_train, labels)

    priors = model.priors
    likelihoods = model.likelihoods

    return model, vocab

def predict(model, data, vocab):
    X_test = text_to_binary_vectors(data, vocab)
    
    predictions = model.predict(X_test)

    return predictions