from .data_utils import build_vocab, text_to_binary_vectors
from .naive_bayes import NaiveBayes # Import NaiveBayes for type hinting if desired


def train(model: NaiveBayes, data, labels):
    # Builds vocabulary, vectorizes data, trains the Naive Bayes model, and returns the trained model and the vocabulary used.
    print("Building vocabulary...")
    vocab = build_vocab(data)

    print("Vectorizing training data...")
    X_train = text_to_binary_vectors(data, vocab)

    print("Fitting model...")
    # Pass the vocabulary to the fit method 
    model.fit(X_train, labels, vocab)
    print("Model fitting complete.")


    return model, vocab # Return the trained model and the vocab

def predict(model: NaiveBayes, data, vocab):
    # Vectorizes test data using the provided vocabulary and makes predictions using the trained model.


    if vocab != model.vocabulary:
        raise ValueError("Vocabulary mismatch between provided vocab and model's internal vocab.")

    print("Vectorizing test data...")
    X_test = text_to_binary_vectors(data, vocab)

    print("Making predictions...")
    predictions = model.predict(X_test)
    print("Prediction complete.")
    return predictions