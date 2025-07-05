import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_model(df):
    X = df.drop(columns=['Driver', 'Position', 'Round'])  # Features
    y = df['Position']  # Target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, 'models/f1_position_predictor.pkl')
    print("✅ Model trained and saved.")
