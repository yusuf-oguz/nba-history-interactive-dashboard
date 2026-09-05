# DataVIZZ — NBA Statistics Dashboard (1947–2024)

İTÜ YZV475E (Data Visualization) dönem projesi. 77 yıllık NBA tarihini kapsayan, **Streamlit ile geliştirilmiş interaktif bir web dashboard'u** — statik notebook grafiklerinin ötesinde, gerçekten çalıştırılabilir/deploy edilebilir bir uygulama.

## Ne Yapıyor

5 sekmeli, her biri farklı bir analiz açısına odaklanan bir NBA istatistik paneli:

| Sekme | İçerik |
|---|---|
| 📈 **Three-Point Revolution** | Üçlük atışının NBA tarihi boyunca nasıl evrildiği |
| 💪 **Physical vs Performance** | Fiziksel özellikler (boy, kilo) ile performans ilişkisi |
| 📊 **Career Arc & Peak Age** | Oyuncuların kariyer eğrisi, zirve yaptıkları yaş |
| 🌍 **Geography** | Oyuncuların doğum yeri — ülke bazlı dünya haritası + ABD eyalet bazlı choropleth (interaktif, Plotly) |
| 🏃 **Position Profiles** | Pozisyona göre istatistiksel profil karşılaştırması |

## Veri

`data/` altında 21 ayrı CSV dosyası (Basketball Reference kaynaklı) — oyuncu bazlı per-game/per-100-possession/play-by-play istatistikleri, takım istatistikleri, draft geçmişi, ödül oylamaları, All-Star seçimleri. Ayrıca oyuncu doğum yerleri (`data_birthplaces/`) ve oyuncu profil verisi (`data_players/`) ayrı veri setleri olarak işlenmiş.

## Mimari

```
datavizprop/
├── app.py                 # Streamlit giriş noktası — 5 sekmeyi bağlar
├── data_loader.py          # Veri yükleme/önbellekleme katmanı
├── tabs/                   # Her sekme kendi modülü (render() fonksiyonu ile)
│   ├── tab_threept.py
│   ├── tab_physical.py
│   ├── tab_career.py
│   ├── tab_geo.py
│   └── tab_positions.py
├── data/ · data_birthplaces/ · data_players/   # Ham veri (CSV)
├── figures/                # Rapor ve sunum için üretilmiş statik görseller
├── report.pdf / report.tex   # Yazılı proje raporu
├── presentation.pptx        # Sunum
└── Project Proposal.pdf     # Başlangıç proje önerisi
```

## Çalıştırma

```bash
cd datavizprop
uv venv --python 3.12 && uv pip install -r requirements.txt
streamlit run app.py
```

## Kullanılan Araçlar

Streamlit (uygulama çatısı), Plotly (interaktif haritalar/grafikler), Pandas/NumPy (veri işleme), Matplotlib/Seaborn/Statsmodels (rapor için statik analiz).
