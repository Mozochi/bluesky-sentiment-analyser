import nltk
from nltk.corpus import stopwords
from tqdm import tqdm

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))


def build_vocab(texts):
    vocab = set()

    for text in tqdm(texts, desc="Building vocabulary..."):
        text = str(text)
        words = text.lower().split() # Splitting the text into words and converting to lowercase for consistency

        # Filtering out stop words
        filtered_words = [word for word in words if word not in stop_words]
        vocab.update(filtered_words)

    return sorted(list(vocab)) # Sorting for consistency 

def text_to_binary_vectors(texts, vocab):
    vectors = []

    for text in tqdm(texts, desc="Vectorizing texts..."):
        text = str(text)
        words = set(text.lower().split()) # Each unique word in the text

        vector = [1 if word in words else 0 for word in vocab]
        vectors.append(vector)
    return vectors