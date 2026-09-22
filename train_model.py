import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# 1. Create dummy financial data for training
data = {
    "income": [50000, 120000, 30000, 85000, 42000, 200000, 60000],
    "credit_score": [600, 750, 520, 710, 590, 820, 640],
    "dti_ratio": [0.4, 0.2, 0.6, 0.3, 0.5, 0.1, 0.35],
    "will_default": [1, 0, 1, 0, 1, 0, 0] # 1 = Default, 0 = Safe
}
df = pd.DataFrame(data)

# 2. Split the data and train the Random Forest Classifier
X = df[["income", "credit_score", "dti_ratio"]]
y = df["will_default"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Export the trained model to the artifacts directory
os.makedirs("artifacts", exist_ok=True)
joblib.dump(model, "artifacts/credit_model.joblib")
print("Success! Model trained and saved to artifacts/credit_model.joblib")