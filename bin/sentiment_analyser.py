from .data_utils import build_vocab, text_to_binary_vectors
from .naive_bayes import NaiveBayes  # Import NaiveBayes for type hinting if desired


def train(model: NaiveBayes, data, labels):
    """
    Train the Naive Bayes model.

    Parameters:
    model (NaiveBayes): The Naive Bayes model to be trained.
    data (list): A list of documents to train the model on.
    labels (list): A list of class labels corresponding to the documents.

    Returns:
    tuple: A tuple containing the trained model and the vocabulary used.
    """
    # Building vocabulary
    vocab = build_vocab(data)

    # Vectorizing training data
    X_train = text_to_binary_vectors(data, vocab)

    # Fitting the model
    model.fit(X_train, labels, vocab)
    print("Model fitting complete.")

    return model, vocab  # Return the trained model and the vocab


def predict(model: NaiveBayes, data, vocab):
    """
    Predict the class labels for the provided data.

    Parameters:
    model (NaiveBayes): The trained Naive Bayes model.
    data (list): A list of documents to be classified.
    vocab (list): The vocabulary used to vectorize the test data.

    Returns:
    list: A list of predicted class labels for the documents.
    """
    # Check if the provided vocabulary matches the model's internal vocabulary
    if vocab != model.vocabulary:
        raise ValueError("Vocabulary mismatch between provided vocab and model's internal vocab.")

    # Vectorizing test data
    X_test = text_to_binary_vectors(data, vocab)

    # Making predictions
    predictions = model.predict(X_test)
    print("Prediction complete.")

    return predictions