import pandas as pd
import numpy as np
import os

data_dir = r"e:\cenka\VeriAnalizi"
games_path = os.path.join(data_dir, "data\Games.csv")
team_stats_path = os.path.join(data_dir, "data\TeamStatistics.csv")

print("Loading data...")
try:
    df_games = pd.read_csv(games_path)
    df_teams = pd.read_csv(team_stats_path)
    print(f"Games data loaded: {df_games.shape}")
    print(f"Team Stats data loaded: {df_teams.shape}")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

print("\n--- Games Data Info ---")
print(df_games.info())
print("\n--- Team Stats Data Info ---")
print(df_teams.info())

print("\n--- Missing Values (Games) ---")
print(df_games.isnull().sum()[df_games.isnull().sum() > 0])
print("\n--- Missing Values (Team Stats) ---")
print(df_teams.isnull().sum()[df_teams.isnull().sum() > 0])

df_games['gameDate'] = pd.to_datetime(df_games['gameDateEst'])
df_teams['gameDate'] = pd.to_datetime(df_teams['gameDateTimeEst'])

df_teams = df_teams.sort_values('gameDate')

key_stats = [
    'fieldGoalsPercentage', 'threePointersPercentage', 'freeThrowsPercentage',
    'reboundsTotal', 'assists', 'steals', 'blocks', 'turnovers', 'pointsInThePaint'
]

print("\nCalculating Rolling Averages...")

df_rolling = df_teams.copy()

roll_window = 10
for col in key_stats:
    df_rolling[f'roll_{col}_{roll_window}'] = df_rolling.groupby('teamId')[col].transform(
        lambda x: x.shift(1).rolling(window=roll_window, min_periods=1).mean()
    )

print("Rolling averages calculated.")


home_stats = df_rolling[df_rolling['home'] == 1].copy()
away_stats = df_rolling[df_rolling['home'] == 0].copy()

feature_cols = [f'roll_{col}_{roll_window}' for col in key_stats]
home_features = home_stats[['gameId', 'teamId', 'win'] + feature_cols].rename(
    columns={col: f'home_{col}' for col in feature_cols}
)
home_features.rename(columns={'teamId': 'homeTeamId', 'win': 'homeWin'}, inplace=True)

away_features = away_stats[['gameId', 'teamId'] + feature_cols].rename(
    columns={col: f'away_{col}' for col in feature_cols}
)
away_features.rename(columns={'teamId': 'awayTeamId'}, inplace=True)

final_df = pd.merge(home_features, away_features, on='gameId', how='inner')

print("\n--- Final Dataset Shape ---")
print(final_df.shape)
print("\n--- Final Dataset Head ---")
print(final_df.head())

print("\n--- Correlation with Target (Home Win) ---")
correlations = final_df.corr()['homeWin'].sort_values(ascending=False)
print(correlations)

print("\nEDA and Initial Feature Engineering Script Completed.")
