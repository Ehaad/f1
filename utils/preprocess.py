import pandas as pd

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Drop rows with missing lap times or positions
    df.dropna(subset=['LapTimeSeconds', 'Position'], inplace=True)

    # average lap time per driver per round
    grouped = df.groupby(['Driver', 'Team', 'Round'], as_index=False).agg({
        'LapTimeSeconds': 'mean',
        'TyreLife': 'mean',
        'Compound': 'first',
        'Position': 'min' 
    })

    # Encode categorical features
    grouped = pd.get_dummies(grouped, columns=['Team', 'Compound'])

    return grouped
