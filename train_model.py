import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load Dataset
df = pd.read_csv("cybercrime_dataset.csv")

X = df["complaint"]
y = df["category"]

# Build Model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train Model
model.fit(X, y)

# Create models folder if it does not exist
os.makedirs("models", exist_ok=True)

# Save trained model
joblib.dump(model, "models/classifier.pkl")

print("Model Trained Successfully!")