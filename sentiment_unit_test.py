from bin import naive_bayes
from bin import data_utils
import numpy as np

trainTexts = [
    "I love pizza",                 # Class 1 (Positive)
    "I enjoy coding",               # Class 1 (Positive)
    "I hate spam notifications",    # Class 0 (Negative)
    "I dislike noisy alerts",       # Class 0 (Negative)
    "I hate rainy days",            # Class 0 (Negative)
    "I love machine learning",      # Class 1 (Positive)
    "I hate sitting in traffic"     # Class 0 (Negative)
        ]
y_train_list = [1, 1, 0, 0, 0, 1, 0]

# Convert y_train to a NumPy array before passing it to the model
y_train = np.array(y_train_list) 

model = naive_bayes.NaiveBayes()

vocab = data_utils.build_vocab(trainTexts)

# Vectorizing training data
X_train = data_utils.text_to_binary_vectors(trainTexts, vocab)

# Fitting the model
model.fit(X_train, y_train, vocab) 
print("Model fitting complete.")

testTexts = ["I love coding", "I hate pizza",]

X_test = data_utils.text_to_binary_vectors(testTexts, vocab)
predictions = model.predict(X_test)

print("Test vectors:", X_test)
final_predictions = []
for i in predictions:
    final_predictions.append(int(predictions[i]))
print("Predictions:", final_predictions)