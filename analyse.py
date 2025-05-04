from bin import naive_bayes
from bin import sentiment_analyser
import os


MODEL_FILEPATH = "sentiment_analyser_model.pkl"

def main():
    ### Try to Load Pre-trained Model
    print(f"Attempting to load model from {MODEL_FILEPATH}...")
    model = naive_bayes.NaiveBayes.load(MODEL_FILEPATH)
    vocab = None

    if model:
        # Model loaded successfully
        print("Model loaded successfully from file.")
        # Retrieve the vocabulary stored within the loaded model
        vocab = model.vocabulary
        print(f"Using vocabulary with {len(vocab)} words from the loaded model.")


    else:
        ### Model Not Found - Train New Model 
        print(f"Model file not found at {MODEL_FILEPATH}. Training a new model...")

        # Training Data
        train_texts = [
            "I love pizza",                 # Class 1 (Positive)
            "I enjoy coding",               # Class 1 (Positive)
            "I hate spam notifications",    # Class 0 (Negative)
            "I dislike noisy alerts",       # Class 0 (Negative)
            "I hate rainy days",            # Class 0 (Negative)
            "I love machine learning",      # Class 1 (Positive)
            "I hate sitting in traffic"     # Class 0 (Negative)
            ]
        y_train = [1, 1, 0, 0, 0, 1, 0] # Labels for the training data

        # Create a new Naive Bayes instance
        nb_instance = naive_bayes.NaiveBayes()

        model, vocab = sentiment_analyser.train(nb_instance, train_texts, y_train)

        ### Save the Newly Trained Model
        print(f"Saving the newly trained model to {MODEL_FILEPATH}...")
        model.save(MODEL_FILEPATH)
        print("Model saved.")

    ### Testing Phase 
    # Checking we have a model and vocabulary before proceeding
    if not model or not vocab:
         raise RuntimeError("Model or vocabulary is not available. Cannot proceed with testing.")

    print("\n--- Testing ---")
    test_data = ["I love coding", "I hate pizza", "I love driving"]

    
    predictions = sentiment_analyser.predict(model, test_data, vocab)

    print("\n--- Predictions ---")
    for i, prediction in enumerate(predictions):
        # Determine sentiment text based on the prediction label (0 or 1)
        sentiment = 'Positive' if prediction == 1 else 'Negative'
        print(f"'{test_data[i]}' --> {sentiment} (Class {prediction})")

if __name__ == '__main__':
    main()
