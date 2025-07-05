import pandas as pd
import joblib

def predict_next_race(year, round_num):
    model = joblib.load("models/f1_position_predictor.pkl")
    df = pd.read_csv("f1_2025_race_data.csv")

    race_df = df[df['Round'] == round_num]
    if race_df.empty:
        print(f"❌ No race data found for round {round_num}")
        return

    grouped = race_df.groupby(['Driver', 'Team'], as_index=False).agg({
        'LapTimeSeconds': 'mean',
        'TyreLife': 'mean',
        'Compound': 'first'
    })

    driver_names = grouped['Driver'].values

    # Prepare input for model
    input_df = pd.get_dummies(grouped.drop(columns='Driver'), columns=['Team', 'Compound'])

    # Align columns with training set
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_features]

    # Predict
    predictions = model.predict(input_df)
    grouped['PredictedPosition'] = predictions
    grouped['Driver'] = driver_names

    # Sort by predicted position
    full_order = grouped.sort_values('PredictedPosition').reset_index(drop=True)
    full_order.index += 1  # Start from position 1

    print(f"\n🏁 Predicted Race Order - silverstone:\n")
    for i, row in full_order.iterrows():
        print(f"{i}. {row['Driver']} (Predicted: {row['PredictedPosition']:.2f})")
