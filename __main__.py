from nltk.corpus import twitter_samples
from bin import naive_bayes
from bin import sentiment_analyser


def main():
    # Temporary data for testing
    train_texts = [
        "I love pizza",                 # Class 1 (Positive)
        "I enjoy coding",               # Class 1 (Positive)
        "I hate spam notifications",    # Class 0 (Negative)
        "I dislike noisy alerts",       # Class 0 (Negative)
        "I hate rainy days",            # Class 0 (Negative)
        "I love machine learning",      # Class 1 (Positive)
        "I hate sitting in traffic"     # Class 0 (Negative)
        ]
    y_train = [1, 1, 0, 0, 0, 1, 0] # Labels for the training data (1 = Positive, 0 = Negative) for each text in train_texts

    nb = naive_bayes.NaiveBayes() # Creating a Naive Bayes model
    
    model, vocab = sentiment_analyser.train(nb, train_texts, y_train) # Training the model

    test_data =  ["I love coding", "I hate pizza",] # Testing data
    predictions = sentiment_analyser.predict(model, test_data, vocab) # Making predictions

    for i, prediction in enumerate(predictions): # Printing the predictions
        print(f"Prediction for '{test_data[i]}': {'Positive' if prediction == 1 else 'Negative'}") 



if __name__ == '__main__':
    main()