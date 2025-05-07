from bin import naive_bayes
from bin import sentiment_analyser
import os
import pandas as pd
from tqdm import tqdm
import time


class model:
    def __init__(self, MODEL_FILEPATH=None):
        self.MODEL_FILEPATH = MODEL_FILEPATH

    def run_model(self, MODEL_FILEPATH, texts: list):
        ### Try to Load Pre-trained Model
        print(f"Attempting to load model from {MODEL_FILEPATH}...")
        loaded_model = naive_bayes.NaiveBayes.load(MODEL_FILEPATH)
        vocab = None

        if loaded_model:
            # Model loaded successfully
            print("Model loaded successfully from file.")
            # Retrieve the vocabulary stored within the loaded model
            vocab = loaded_model.vocabulary
            print(f"Using vocabulary with {len(vocab)} words from the loaded model.")
            current_model = loaded_model


        else:
            ### Model Not Found - Train New Model 
            print(f"Model file not found at {MODEL_FILEPATH}. Training a new model...")

            # Training Data
            
            try:
                df = pd.read_csv('training.csv')
                sentiment_col_idx = df.columns.get_loc('sentiment')
            except FileNotFoundError:
                print(f"Error: 'training.csv' not found at {MODEL_FILEPATH}. Cannot train a new model...")
                return "Error: Training data not found. Cannot proceed."
            except KeyError:
                print("Error: 'sentiment' column not found in DataFrame.")
                return "Error: 'sentiment' column not found in DataFrame. Cannot proceed"


            train_texts = df['text']
            y_train = df['sentiment'].copy()

            for idx, sentiment_val in enumerate(tqdm(y_train, desc="Updating sentiment column...")):

                if isinstance(sentiment_val, str):
                    sentiment_lower = sentiment_val.lower()

                    if sentiment_lower == "positive":
                        df.iat[idx, sentiment_col_idx] = 2
                    elif sentiment_lower == "neutral":
                        df.iat[idx, sentiment_col_idx] = 1
                    elif sentiment_lower == "negative":
                        df.iat[idx, sentiment_col_idx] = 0

            # Updating y_train after modification to data
            y_train = df['sentiment'].astype(int)
                    

            # Create a new Naive Bayes instance
            nb_instance = naive_bayes.NaiveBayes()

            current_model, vocab = sentiment_analyser.train(nb_instance, train_texts, y_train)

            ### Save the Newly Trained Model
            print(f"Saving the newly trained model to {MODEL_FILEPATH}...")
            model.save(MODEL_FILEPATH)
            print("Model saved.")

        ### Testing Phase 
        # Checking we have a model and vocabulary before proceeding
        if not model or not vocab:
            raise RuntimeError("Model or vocabulary is not available. Cannot proceed with testing.")

        print("\n--- Testing ---")
        predictions = sentiment_analyser.predict(current_model, texts, vocab)


        print("\n--- Predictions ---")
        results = []
        for i, prediction in enumerate(predictions):
            original_text = texts[i]
            # Determine sentiment text based on the prediction label (0 (Negative) or 1 (1 Positive))
            if prediction == 1:
                sentiment = "Neutral"
            elif prediction == 2:
                sentiment = "Positive"
            else:
                sentiment = "Negative"

            try:
                print(f"'{original_text}' ---> {prediction} ({sentiment})")
            except UnicodeEncodeError:
                try:
                    cli_safe_text = original_text.encode('cp1252', errors='replace').decode('cp1252')

                    display_log_text = (cli_safe_text[:60] + '...') if len(cli_safe_text) > 60 else cli_safe_text
                    print(f"'{display_log_text}' ---> {prediction} ({sentiment})")

                except Exception as e_log_fallback:
                    print(f"Prediction {prediction} ({sentiment}) for text item {i}. Error during logging: {e_log_fallback}")
            except Exception as e_outer_log:
                print(f"Prediction {prediction} ({sentiment}) for text item {i}. Error: {e_outer_log}")
            

            display_text = (original_text[:70] + '...') if len(original_text) > 70 else original_text

            results.append(f"Text: '{display_text}'\nSentiment:{sentiment}\n\n-------------------------------------------------------------\n")

        if not results:
            return ["No predictions were made."]
        return results


if __name__ == '__main__':
    print("Do not run analyse.py directly. Instead run controller.py.")