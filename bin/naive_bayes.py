import math
import os 
from tqdm import tqdm
import json

from bin.config import smoothingFactor

class NaiveBayes:
    def __init__(self, smoothing=smoothingFactor):
        self.priors = {}
        self.likelihoods = {}
        self.smoothing = smoothing
        self.classes = set()
        self.vocabulary = []

    def fit(self, X, y, vocabulary):
        self.vocabulary = vocabulary # Store the vocabulary
        totalDocuments = len(y)
        self.classes = set(y)

        if totalDocuments == 0:
            print("Warning: Training data is empty.")

        # Counting how many times class c appears in y
        for classLabel in self.classes:
            documentsInClass = (y == classLabel).sum()
            self.priors[classLabel] = documentsInClass / totalDocuments

        numFeatures = len(self.vocabulary) # Use stored vocabulary length
        for classLabel in tqdm(self.classes, desc="Calculating Likelihoods..."):
            # Initialize likelihoods for this class using feature indices (0 to numFeatures-1)
            self.likelihoods[classLabel] = {} # Dictionary mapping feature index : likelihood

            # All the feature vectors for this class
            classDocuments = [X[i] for i in range(totalDocuments) if y[i] == classLabel]
            numDocumentsInClass = len(classDocuments)

            # For each feature position (index corresponding to a word in vocabulary)
            for featurePosition in tqdm(range(numFeatures), desc=f"Likelihoods class {classLabel}...", leave=False):
                # Counting how many times this feature is 1 for this class
                featurePositiveCount = sum(1 for document in classDocuments if document[featurePosition] == 1)

                # Laplace Smoothing (positive count + smoothing) / (class documents + smoothing * 2 possible values (0 or 1))
                self.likelihoods[classLabel][featurePosition] = (featurePositiveCount + self.smoothing) / (numDocumentsInClass + self.smoothing * 2)

    def predict(self, X):
        # Handling for edge cases
        if not self.priors or not self.likelihoods or not self.vocabulary or not self.classes:
            raise ValueError("Model attributes (priors, likelihoods, vocabulary, classes) are not properly initialized. Train or load the model first.")

        predictions = []
        # Use tqdm for the prediction loop
        for document in tqdm(X, desc="Predicting       "):
            scores = {}
            for classLabel in self.classes:
                # Initialize score with log prior probability
                prior = self.priors.get(classLabel, 0) # Get prior, default 0 if missing
                if prior <= 0:
                    log_prior = -float('inf') # Avoid log(0)
                else:
                    log_prior = math.log(prior)
                score = log_prior

                if classLabel not in self.likelihoods:
                    print(f"Warning: Likelihoods missing for class {classLabel} during prediction. Assigning -inf score.")
                    scores[classLabel] = -float('inf')
                    continue 

                class_likelihoods = self.likelihoods[classLabel]

                # Add log likelihood for each feature
                for featurePosition, featureValue in enumerate(document):
                    # Boundary check for safety
                    if featurePosition >= len(self.vocabulary):
                        print(f"Warning: Feature position {featurePosition} out of bounds for vocabulary (size {len(self.vocabulary)}). Skipping feature.")
                        continue

                    # Get P(feature=1|class) 
                    likelihood_feature_1 = class_likelihoods.get(featurePosition)

                    # Handle missing likelihood for a specific feature (if vocab changed or load issue)
                    if likelihood_feature_1 is None:
                        print(f"Warning: Likelihood missing for feature {featurePosition} in class {classLabel}. Using default smoothed value.")
                        # Fallback to default smoothed probability (0.5 if smoothing=1)
                        likelihood_feature_1 = self.smoothing / (self.smoothing * 2.0)

                    # Add log probability based on actual feature value (0 or 1)
                    if featureValue == 1:
                        if likelihood_feature_1 > 0:
                            score += math.log(likelihood_feature_1)
                        else:
                            score += -float('inf') # Avoiding log(0)
                    else: # featureValue == 0
                        # P(feature=0|class) = 1 - P(feature=1|class)
                        prob_neg = 1.0 - likelihood_feature_1
                        if prob_neg > 0:
                            score += math.log(prob_neg)
                        else:
                            score += -float('inf') # Avoid log(0)

                scores[classLabel] = score

            # Choose class with highest log probability score
            if not scores or all(s == -float('inf') for s in scores.values()):
                # Handle case where all scores are -inf
                predictedClass = list(self.classes)[0] if self.classes else None # Default
                print(f"Warning: All class scores are -inf for a document. Defaulting to {predictedClass}.")
            else:
                predictedClass = max(scores, key=scores.get)

            predictions.append(predictedClass)

        return predictions


    def save(self, filepath):
        # Saves the model's essential data to a JSON file.
        print(f"Saving model state to {filepath}...")

        # Prepare likelihoods with string keys for JSON compatibility
        # Outer keys (class labels) and inner keys (feature indices) must be strings
        likelihoods_json = {}
        for class_label, feature_probs in self.likelihoods.items():
            likelihoods_json[str(class_label)] = {str(feat_idx): prob
                                                  for feat_idx, prob in feature_probs.items()}

        # Prepare priors with string keys
        priors_json = {str(k): v for k, v in self.priors.items()}

        # Bundle all necessary data into a dictionary
        model_data = {
            "model_type": "NaiveBayes",
            "smoothing": self.smoothing,
            "vocabulary": self.vocabulary,
            "classes": list(self.classes), # Convert set to list for JSON
            "priors": priors_json,
            "likelihoods": likelihoods_json
        }

        try:

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(model_data, f, indent=4) 
            print("Model state saved successfully.")
        except IOError as e:
            print(f"Error saving model state to {filepath}: {e}")
        except TypeError as e:
             print(f"Error: Could not serialize model data to JSON: {e}")

    @staticmethod
    def load(filepath):
        # Loads model state from a JSON file and returns a new NaiveBayes instance.
        if not os.path.exists(filepath):
            return None

        print(f"Loading model state from {filepath}...")
        try:

            with open(filepath, 'r', encoding='utf-8') as f:
                model_data = json.load(f)

            ### Data Validation ###
            required_keys = ["smoothing", "vocabulary", "classes", "priors", "likelihoods"]
            if not all(key in model_data for key in required_keys):
                 raise ValueError(f"JSON file {filepath} is missing required keys.")
            if model_data.get("model_type") != "NaiveBayes":
                 print(f"Warning: JSON file {filepath} model_type is not 'NaiveBayes'.")


            ### Create and Populate New Instance ###

            loaded_smoothing = model_data.get("smoothing", smoothingFactor)
            model = NaiveBayes(smoothing=loaded_smoothing)

            model.vocabulary = model_data.get("vocabulary", [])

            # Load classes and convert back to set
            loaded_classes = model_data.get("classes", [])
            try:
                model.classes = set(int(c) for c in loaded_classes)
            except (ValueError, TypeError) as e:
                 print(f"Warning: Error converting loaded classes {loaded_classes} to set of integers: {e}. Using empty set.")
                 model.classes = set()

            # Load priors and convert keys back to int
            loaded_priors = model_data.get("priors", {})
            try:
                model.priors = {int(k): v for k, v in loaded_priors.items()}
            except (ValueError, TypeError) as e:
                 print(f"Warning: Error converting loaded prior keys to integers: {e}. Priors may be incorrect.")
                 model.priors = {} 


            # Load likelihoods and convert keys back to int
            loaded_likelihoods = model_data.get("likelihoods", {})
            model.likelihoods = {}
            try:
                 # Outer keys are class labels (str -> int)
                 # Inner keys are feature positions (str -> int)
                for class_label_str, feature_probs_str in loaded_likelihoods.items():
                    class_label_int = int(class_label_str)
                    model.likelihoods[class_label_int] = {int(feat_idx_str): prob
                                                         for feat_idx_str, prob in feature_probs_str.items()}
            except (ValueError, TypeError) as e:
                print(f"Warning: Error converting loaded likelihood keys to integers: {e}. Likelihoods may be incomplete.")


            print("Model state loaded successfully.")
            return model

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading or parsing model state from {filepath}: {e}")
            return None
        except (ValueError, TypeError, KeyError) as e: 
             print(f"Error reconstructing model from data in {filepath}: {e}")
             return None
        except Exception as e: 
             print(f"An unexpected error occurred during model loading: {e}")
             return None