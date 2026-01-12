import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

try:
    df_games = pd.read_csv('Games.csv')
    print("--- GAMES DATA INFO ---")
    print(df_games.info())
    print("\n--- GAMES HEAD ---")
    print(df_games.head())
    
    print("\n--- MISSING VALUES ---")
    print(df_games.isnull().sum())

except Exception as e:
    print(f"Error reading Games.csv: {e}")
