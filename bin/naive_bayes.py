import math
import os
import json
from tqdm import tqdm

from bin.config import smoothingFactor


class NaiveBayes:
    def __init__(self, smoothing=smoothingFactor):
        self.priors = {}
        self.likelihoods = {}
        self.smoothing = smoothing
        self.classes = set()
        self.vocabulary = []

    def fit(self, X, y, vocabulary):
        """
        Train the NaiveBayes model using the provided data.

        Parameters:
        X (list): List of feature vectors (documents).
        y (list): List of class labels corresponding to the documents.
        vocabulary (list): The vocabulary used for feature extraction.

        Returns:
        None
        """
        self.vocabulary = vocabulary  # Store the vocabulary
        total_documents = len(y)
        self.classes = set(y)

        if total_documents == 0:
            print("Warning: Training data is empty.")

        # Counting how many times each class appears in y
        for class_label in self.classes:
            documents_in_class = (y == class_label).sum()
            self.priors[class_label] = documents_in_class / total_documents

        num_features = len(self.vocabulary)  # Use stored vocabulary length
        for class_label in tqdm(self.classes, desc="Calculating Likelihoods..."):
            # Initialize likelihoods for this class using feature indices (0 to num_features-1)
            self.likelihoods[class_label] = {}  # Dictionary mapping feature index : likelihood

            # All the feature vectors for this class
            class_documents = [X[i] for i in range(total_documents) if y[i] == class_label]
            num_documents_in_class = len(class_documents)

            # For each feature position (index corresponding to a word in vocabulary)
            for feature_position in tqdm(range(num_features), desc=f"Likelihoods class {class_label}...", leave=False):
                # Counting how many times this feature is 1 for this class
                feature_positive_count = sum(1 for document in class_documents if document[feature_position] == 1)

                # Laplace Smoothing (positive count + smoothing) / (class documents + smoothing * 2 possible values (0 or 1))
                self.likelihoods[class_label][feature_position] = (feature_positive_count + self.smoothing) / \
                                                                   (num_documents_in_class + self.smoothing * 2)

    def predict(self, X):
        """
        Predict the class labels for the provided feature vectors.

        Parameters:
        X (list): List of feature vectors (documents).

        Returns:
        list: Predicted class labels for each document.
        """
        # Handling for edge cases
        if not self.priors or not self.likelihoods or not self.vocabulary or not self.classes:
            raise ValueError("Model attributes (priors, likelihoods, vocabulary, classes) are not properly initialized. "
                             "Train or load the model first.")

        predictions = []
        for document in tqdm(X, desc="Predicting"):
            scores = {}
            for class_label in self.classes:
                # Initialize score with log prior probability
                prior = self.priors.get(class_label, 0)  # Get prior, default 0 if missing
                log_prior = math.log(prior) if prior > 0 else -float('inf')
                score = log_prior

                if class_label not in self.likelihoods:
                    print(f"Warning: Likelihoods missing for class {class_label} during prediction. Assigning -inf score.")
                    scores[class_label] = -float('inf')
                    continue

                class_likelihoods = self.likelihoods[class_label]

                # Add log likelihood for each feature
                for feature_position, feature_value in enumerate(document):
                    # Boundary check for safety
                    if feature_position >= len(self.vocabulary):
                        print(f"Warning: Feature position {feature_position} out of bounds for vocabulary (size {len(self.vocabulary)}). Skipping feature.")
                        continue

                    # Get P(feature=1|class)
                    likelihood_feature_1 = class_likelihoods.get(feature_position)

                    # Handle missing likelihood for a specific feature (if vocab changed or load issue)
                    if likelihood_feature_1 is None:
                        print(f"Warning: Likelihood missing for feature {feature_position} in class {class_label}. Using default smoothed value.")
                        likelihood_feature_1 = self.smoothing / (self.smoothing * 2.0)

                    # Add log probability based on actual feature value (0 or 1)
                    if feature_value == 1:
                        score += math.log(likelihood_feature_1) if likelihood_feature_1 > 0 else -float('inf')
                    else:  # feature_value == 0
                        prob_neg = 1.0 - likelihood_feature_1
                        score += math.log(prob_neg) if prob_neg > 0 else -float('inf')

                scores[class_label] = score

            # Choose class with highest log probability score
            predicted_class = max(scores, key=scores.get) if not all(s == -float('inf') for s in scores.values()) else list(self.classes)[0]
            predictions.append(predicted_class)

        return predictions

    def save(self, filepath):
        """
        Save the trained model to a file.

        Parameters:
        filepath (str): The path to save the model.

        Returns:
        None
        """
        print(f"Saving model state to {filepath}...")

        # Prepare likelihoods with string keys for JSON compatibility
        likelihoods_json = {str(class_label): {str(feat_idx): prob for feat_idx, prob in feature_probs.items()}
                            for class_label, feature_probs in self.likelihoods.items()}

        # Prepare priors with string keys
        priors_json = {str(k): v for k, v in self.priors.items()}

        # Bundle all necessary data into a dictionary
        model_data = {
            "model_type": "NaiveBayes",
            "smoothing": self.smoothing,
            "vocabulary": self.vocabulary,
            "classes": list(self.classes),
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
        """
        Load a model from a file.

        Parameters:
        filepath (str): The path from where to load the model.

        Returns:
        NaiveBayes: The loaded NaiveBayes model instance.
        """
        if not os.path.exists(filepath):
            return None

        print(f"Loading model state from {filepath}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                model_data = json.load(f)

            required_keys = ["smoothing", "vocabulary", "classes", "priors", "likelihoods"]
            if not all(key in model_data for key in required_keys):
                raise ValueError(f"JSON file {filepath} is missing required keys.")

            if model_data.get("model_type") != "NaiveBayes":
                print(f"Warning: JSON file {filepath} model_type is not 'NaiveBayes'.")

            model = NaiveBayes(smoothing=model_data.get("smoothing", smoothingFactor))
            model.vocabulary = model_data.get("vocabulary", [])
            model.classes = set(int(c) for c in model_data.get("classes", []))
            model.priors = {int(k): v for k, v in model_data.get("priors", {}).items()}

            # Load likelihoods and convert keys back to int
            model.likelihoods = {
                int(class_label_str): {int(feat_idx_str): prob for feat_idx_str, prob in feature_probs_str.items()}
                for class_label_str, feature_probs_str in model_data.get("likelihoods", {}).items()
            }

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
