from bin import naive_bayes
from bin import sentiment_analyser
import os
import pandas as pd
from tqdm import tqdm
import time


MODEL_FILEPATH = "sentiment_analyser_model.json"

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
        df = pd.read_csv('training.csv')
        
        try:
            sentiment_col_idx = df.columns.get_loc('sentiment')
        except KeyError:
            print("Error: 'sentiment' column not found in DataFrame.")
            exit()


        train_texts = df['text']
        y_train = df['sentiment']

        for idx, sentiment in enumerate(tqdm(y_train, desc="Updating sentiment column...")):

            if isinstance(sentiment, str):
                sentiment_lower = sentiment.lower()

                if sentiment_lower == "positive":
                    df.iat[idx, sentiment_col_idx] = 2
                elif sentiment_lower == "neutral":
                    df.iat[idx, sentiment_col_idx] = 1
                elif sentiment_lower == "negative":
                    df.iat[idx, sentiment_col_idx] = 0


                

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
    test_data = ["Gaming is good", "i hate the internet"]

    
    predictions = sentiment_analyser.predict(model, test_data, vocab)

    print("\n--- Predictions ---")
    for i, prediction in enumerate(predictions):
        # Determine sentiment text based on the prediction label (0 (Negative) or 1 (1 Positive))
        if prediction == 1:
            sentiment = "Neutral"
        elif prediction == 2:
            sentiment = "Positive"
        else:
            sentiment = "Negative"
        print(f"'{test_data[i]}' --> {prediction} ({sentiment})")

if __name__ == '__main__':
    main()