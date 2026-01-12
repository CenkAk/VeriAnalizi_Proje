
import pandas as pd
import numpy as np

def load_and_process_player_stats():
    print("PlayerStatistics.csv yükleniyor...")
    try:
        df_players = pd.read_csv('data\PlayerStatistics.csv')
    except FileNotFoundError:
        print("PlayerStatistics.csv not found.")
        return

    print("Tarihler ayrılıyor...")
    df_players['gameDateTimeEst'] = pd.to_datetime(df_players['gameDateTimeEst'], format='mixed', utc=True)

    print("Veri sıralanıyor...")
    df_players = df_players.sort_values(by=['personId', 'gameDateTimeEst'])

    metrics = ['points', 'assists', 'reboundsTotal', 'steals', 'blocks', 'plusMinusPoints']
    
    df_players[metrics] = df_players[metrics].fillna(0)

    rolling_features = df_players.groupby('personId')[metrics].apply(
        lambda x: x.shift(1).rolling(window=10, min_periods=1).mean()
    )
    
    rolling_features.columns = [f'player_rolling_mean_{col}' for col in metrics]
    
    df_players = pd.concat([df_players, rolling_features], axis=1)

    print("Oyun ve Takım bazlı toplama yapılıyor...")
    
    agg_funcs = {
        f'player_rolling_mean_{col}': ['mean', 'max'] for col in metrics
    }
    
    team_player_stats = df_players.groupby(['gameId', 'playerteamName']).agg(agg_funcs)
    
    team_player_stats.columns = ['_'.join(col).strip() for col in team_player_stats.columns.values]
    team_player_stats = team_player_stats.reset_index()
    
    print("Toplama tamamlandı.")
    print("\nÖrnek Toplanmış Veri:")
    print(team_player_stats.head())
    
    print(f"\nToplanmış veri toplam satır sayısı: {len(team_player_stats)}")
    
    return team_player_stats

if __name__ == "__main__":
    df_res = load_and_process_player_stats()
    if df_res is not None:
        df_res.to_csv('processed_player_stats_preview.csv', index=False)
        print("Önizleme verisi 'processed_player_stats_preview.csv' olarak kaydedildi.")
