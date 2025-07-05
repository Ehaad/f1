from utils.preprocess import preprocess_data
from utils.train_model import train_model
from utils.predict import predict_next_race

df = preprocess_data("f1_2025_race_data.csv")
train_model(df)

# Predict full race order for latest round
predict_next_race(2025, 11) 
