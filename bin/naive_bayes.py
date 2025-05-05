import math
import pickle
import os 
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
        self.vocabulary = vocabulary # Store the vocabulary
        totalDocuments = len(y)
        self.classes = set(y)

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
        if not self.priors or not self.likelihoods or not self.vocabulary:
            raise ValueError("Model must be trained with fit() or loaded before calling predict()")

        predictions = []
        for document in tqdm(X, desc="Predicting...    "): # Classify each document
            scores= {}

            # For each possible class identified during training
            for classLabel in self.classes:
                # Start with log of the prior probability
                # Check if prior is zero, handle with a very small number or error
                if self.priors[classLabel] <= 0:
                     # Avoid log(0) - assign a very small log probability
                    score = -float('inf') 
                else:
                    score = math.log(self.priors[classLabel])

                # Add the log of the likelihood of each feature
                for featurePosition, featureValue in enumerate(document):
                    # Ensure featurePosition is within the bounds of likelihoods learned
                    if featurePosition >= len(self.vocabulary):
                         # This shouldn't happen if vectorization uses the model's vocabulary
                         print(f"Warning: Feature position {featurePosition} out of bounds for learned vocabulary (size {len(self.vocabulary)}). Skipping.")
                         continue

                    likelihood = self.likelihoods[classLabel][featurePosition]

                    # Avoid log(0) for likelihoods as well
                    if featureValue == 1:
                        score += math.log(likelihood) if likelihood > 0 else -float('inf')
                    else:
                        # P(feature=0|class) = 1 - P(feature=1|class)
                        prob_neg = 1.0 - likelihood
                        score += math.log(prob_neg) if prob_neg > 0 else -float('inf')

                scores[classLabel] = score

            # Handle case where all scores might be -inf
            if not scores or all(s == -float('inf') for s in scores.values()):
                # Default prediction or raise error, here we'll arbitrarily pick the first class
                predictedClass = list(self.classes)[0] if self.classes else None
                print(f"Warning: Could not determine best class for document (all scores -inf). Defaulting to {predictedClass}")
            else:
                # Pick the class with the highest log-probability score
                predictedClass = max(scores, key=scores.get) # Simplified max finding

            predictions.append(predictedClass)

        return predictions

    def save(self, filepath):
        # Saves the trained NaiveBayes model instance to a file using pickle
        print(f"Saving model to {filepath}...")
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print("Model saved.")

    @staticmethod
    def load(filepath):
        # Loads the Naive Bayes model instance from a file using pickle
        if os.path.exists(filepath):
            print(f"Loading model from {filepath}...")
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
            print("Model loaded.")
            # Basic check to ensure it looks like our model
            if not isinstance(model, NaiveBayes):
                 raise TypeError(f"Loaded object from {filepath} is not a NaiveBayes instance.")
            # Ensure essential attributes are present
            if not hasattr(model, 'priors') or not hasattr(model, 'likelihoods') or not hasattr(model, 'vocabulary'):
                 raise ValueError(f"Loaded model from {filepath} is missing essential attributes.")
            return model
        else:
            print(f"Model file not found at {filepath}. Need to train a new model.")
            return None