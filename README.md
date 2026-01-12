# NBA Maç Sonucu Tahmini Projesi

Bu proje, Kaggle üzerinden alınan **Historical NBA Data** veri seti kullanılarak NBA maçlarının sonuçlarını tahmin etmeye yönelik makine öğrenmesi modelleri geliştirmeyi amaçlamaktadır.

## Proje Hakkında

**Hedef Problem:** Sınıflandırma (Classification)
- **Hedef Değişken:** Ev sahibi takımın maçı kazanıp kazanmayacağı (`HomeWin`: 1 = Kazandı, 0 = Kaybetti)

**Veri Seti:**
- Kaggle'dan alınan Historical NBA Data
- 72,470 maç verisi
- `Games.csv`: Maç genel bilgileri (17 kolon)
- `TeamStatistics.csv`: Takım istatistikleri/Box Score verileri (48 kolon)

## Kurulum

### Gereksinimler

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız var:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### Veri Seti

Veri setleri `data/` klasöründe bulunmalıdır:
- `data/Games.csv` - Maç genel bilgileri
- `data/TeamStatistics.csv` - Takım istatistikleri
- `data/final_processed_data.csv` - İşlenmiş final veri seti (notebook bu dosyayı kullanır)

## Kullanım

### Jupyter Notebook ile Çalıştırma

Ana analiz `nba_projesi.ipynb` dosyasında bulunmaktadır:

```bash
jupyter notebook nba_projesi.ipynb
```

### Python Scriptleri

Proje ayrıca çeşitli Python scriptleri içerir:
- `run_full_pipeline.py`: Tam veri işleme hattı
- `eda_script.py`: Exploratory Data Analysis scripti
- `eda_feature_engineering.py`: Feature engineering scripti
- `process_player_stats.py`: Oyuncu istatistikleri işleme

## Yöntem

### Veri İşleme

1. **Veri Yükleme:** Games ve TeamStatistics verilerinin yüklenmesi
2. **Feature Engineering:** 
   - Rolling averages (son 10 maç ortalaması)
   - Takım istatistiklerinin birleştirilmesi
3. **Veri Ön İşleme:**
   - Eksik veri kontrolü
   - Özellik seçimi: Sadece sayısal kolonlar kullanılmıştır (string/tarih kolonları ve ID kolonları hariç tutulmuştur)
   - Normalizasyon (StandardScaler)

### Kullanılan Modeller

1. **Logistic Regression** - Doğrusal sınıflandırma modeli
2. **K-Nearest Neighbors (KNN)** - K=15 parametresi ile
3. **Support Vector Machine (SVM)** - Linear kernel ile
4. **Decision Tree** - Max depth=5 ile

### Değerlendirme Metrikleri

- Accuracy (Doğruluk)
- Classification Report (Precision, Recall, F1-Score)
- Confusion Matrix

## Sonuçlar

### Model Başarı Oranları

| Model | Accuracy |
|-------|----------|
| Logistic Regression | **62.9%** |
| SVM | 61.4% |
| KNN | 56.3% |
| Decision Tree | 49.9% |

**En İyi Model:** Logistic Regression (%62.9 accuracy)

### Bulgular

- Logistic Regression modeli en yüksek başarı oranına sahiptir
- Ev sahibi takım avantajı (home court advantage) faktörü önemli bir rol oynamaktadır
- Rolling averages ile oluşturulan özellikler model performansını artırmaktadır

## Proje Yapısı

```
VeriAnalizi/
├── data/                          # Veri setleri
│   ├── Games.csv
│   ├── TeamStatistics.csv
│   └── final_processed_data.csv   # İşlenmiş veri (notebook bunu kullanır)
├── nba_projesi.ipynb              # Ana Jupyter Notebook
└── README.md                      # Bu dosya
```

## EDA (Exploratory Data Analysis)

Proje kapsamında aşağıdaki görselleştirmeler yapılmıştır:
- Eksik veri analizi
- Hedef değişken dağılımı (HomeWin)
- Sayısal özelliklerin dağılım grafikleri (histogram)
- Aykırı değer analizi (boxplot)
- Korelasyon heatmap
- Confusion Matrix görselleştirmeleri

## İlgili Linkler

- **Kaggle Veri Seti:** [Historical NBA Data](https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores)
- **GitHub Repository:** (GitHub repo linki buraya eklenecek)