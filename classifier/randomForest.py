import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from utils import extract_features
import os

# Încarcă datasetul
df = pd.read_csv("/Users/user/Documents/GitHub/SecureME/dataset/malicious_phish.csv")  # schimbă cu calea reală

# Encode label (dacă nu e deja făcut)
label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['type'])

# Echilibrare set (sampling)
df_benign = df[df['label_encoded'] == 0].sample(100000, random_state=24)
df_phishing = df[df['label_encoded'] == 1]
df_defacement = df[df['label_encoded'] == 3]
df_malware = df[df['label_encoded'] == 2]

df_balanced = pd.concat([df_benign, df_phishing, df_defacement, df_malware]).reset_index(drop=True)

# Extrage features
features_df = df_balanced['url'].apply(extract_features)
df_balanced = pd.concat([df_balanced, features_df], axis=1)

# Define features și target
X = df_balanced.drop(columns=['url', 'type', 'label_encoded'])
y = df_balanced['label_encoded']

# Salvează numele coloanelor de feature
feature_names = X.columns.tolist()

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelul
clf = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)

clf.fit(X_train, y_train)

print("Accuracy on train set:", clf.score(X_train, y_train))
print("Accuracy on test set:", clf.score(X_test, y_test))

# Creează folder dacă nu există
os.makedirs("randomForestV2", exist_ok=True)

# Salvează modelul și obiectele auxiliare
joblib.dump(clf, "randomForestV2/rf_model.pkl")
joblib.dump(feature_names, "randomForestV2/selected_columns.pkl")
joblib.dump(label_encoder, "randomForestV2/label_encoder.pkl")
