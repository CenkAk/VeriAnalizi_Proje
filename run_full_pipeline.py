import pandas as pd
import numpy as np
import os

def run_pipeline():
    print("=== NBA Veri İşleme Hattı Başlatılıyor ===")
    
    print("\n1. Veri Setleri Yükleniyor...")
    games_path = 'data/Games.csv'
    teams_path = 'data/TeamStatistics.csv'
    
    try:
        df_games = pd.read_csv(games_path)
        df_teams = pd.read_csv(teams_path)
        print("Games ve TeamStatistics yüklendi.")
    except Exception as e:
        print(f"Hata: Dosyalar bulunamadı: {e}")
        return

    df_games['gameDateTimeEst'] = pd.to_datetime(df_games['gameDateTimeEst'], format='mixed', utc=True)
    df_teams['gameDateTimeEst'] = pd.to_datetime(df_teams['gameDateTimeEst'], format='mixed', utc=True)
    
    df_teams = df_teams.sort_values('gameDateTimeEst')
    df_games = df_games.sort_values('gameDateTimeEst')

    print("\n2. Takım İstatistikleri (Rolling Features) Hesaplanıyor...")
    
    team_metrics = [
        'assists', 'blocks', 'steals', 
        'fieldGoalsPercentage', 'threePointersPercentage', 'freeThrowsPercentage',
        'reboundsTotal', 'turnovers', 'plusMinusPoints', 'pointsInThePaint'
    ]
    
    team_metrics = [col for col in team_metrics if col in df_teams.columns]
    
    df_teams_rolling = df_teams.groupby('teamId')[team_metrics].transform(
        lambda x: x.shift(1).rolling(window=10, min_periods=1).mean()
    )
    
    df_teams_rolling.columns = [f'team_rolling_{col}' for col in df_teams_rolling.columns]
    
    df_teams_with_features = pd.concat([df_teams[['gameId', 'teamId']], df_teams_rolling], axis=1)

    print("\n4. Tüm Veriler Birleştiriliyor (Merging)...")
    
    final_df = df_games.copy()
    
    final_df = pd.merge(
        final_df,
        df_teams_with_features.add_prefix('home_'),
        left_on=['gameId', 'hometeamId'],
        right_on=['home_gameId', 'home_teamId'],
        how='left'
    )
    
    final_df = pd.merge(
        final_df,
        df_teams_with_features.add_prefix('away_'),
        left_on=['gameId', 'awayteamId'],
        right_on=['away_gameId', 'away_teamId'],
        how='left'
    )
    
    print(f"NaN öncesi boyut: {final_df.shape}")
    final_df = final_df.dropna()
    print(f"NaN sonrası boyut: {final_df.shape}")
    
    output_path = 'data/final_processed_data.csv'
    print(f"\n5. Veri Kaydediliyor: {output_path}")
    final_df.to_csv(output_path, index=False)
    print("İşlem Başarıyla Tamamlandı!")

if __name__ == "__main__":
    run_pipeline()
