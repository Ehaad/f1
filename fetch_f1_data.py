import fastf1
import pandas as pd

fastf1.Cache.enable_cache('f1_cache')

def fetch_2025_data():
    race_data = []
    qual_data = []

    for rnd in range(1, 24):

        try:
            print(f"🔄 Fetching Round {rnd}...")

            # Fetch race session
            race = fastf1.get_session(2025, rnd, 'R')
            race.load()
            laps = race.laps.dropna(subset=['LapTime'])

            if laps.empty:
                print(f"⚠️ No race data for round {rnd}")
                continue

            laps['Year'] = 2024
            laps['Round'] = rnd
            laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
            race_data.append(laps[['Driver', 'Team', 'Compound', 'TyreLife', 'Position', 'LapTimeSeconds', 'Year', 'Round']])

            # Fetch qualifying session
            quali = fastf1.get_session(2024, rnd, 'Q')
            quali.load()
            q_df = quali.results[['Driver', 'Position']].copy()
            q_df.columns = ['Driver', 'QualifyingPosition']
            q_df['Year'] = 2025
            q_df['Round'] = rnd
            qual_data.append(q_df)

            print(f"✅ Successfully fetched Round {rnd}")

        except Exception as e:
            print(f"❌ Skipped Round {rnd}: {e}")

    # Save only if data exists
    if race_data:
        pd.concat(race_data).to_csv("f1_2025_race_data.csv", index=False)
        print("📁 Saved race data → f1_2025_race_data.csv")
    else:
        print("⚠️ No race data fetched.")

    if qual_data:
        pd.concat(qual_data).to_csv("qualifying.csv", index=False)
        print("📁 Saved qualifying data → qualifying.csv")
    else:
        print("⚠️ No qualifying data fetched.")

if __name__ == "__main__":
    fetch_2025_data()
