# DataVIZZ: NBA Statistics Dashboard (1947-2024)

<details>
<summary>🇹🇷 Türkçe özet için tıklayın</summary>

3 kişilik bir takım projesi (Nurettin Macit, Mehmet Arda Öncel, Yusuf Oğuz). 77 yıllık NBA tarihini kapsayan, **Streamlit ile geliştirilmiş interaktif bir web dashboard'u**, statik notebook grafiklerinin ötesinde gerçekten çalıştırılabilir/deploy edilebilir bir uygulama.

5 sekme: üçlük atışının NBA tarihi boyunca evrimi, fiziksel özellikler ile performans ilişkisi, oyuncuların kariyer eğrisi ve zirve yaptıkları yaş, oyuncuların doğum yeri (ülke haritası + ABD eyalet bazlı interaktif choropleth), pozisyona göre istatistiksel profil karşılaştırması.

`data/` altında 21 ayrı CSV dosyası (Basketball Reference kaynaklı): oyuncu bazlı per-game/per-100-possession/play-by-play istatistikleri, takım istatistikleri, draft geçmişi, ödül oylamaları, All-Star seçimleri. Ayrıca oyuncu doğum yerleri ve oyuncu profil verisi ayrı veri setleri olarak işlenmiş.

Çalıştırmak için: `cd datavizprop && uv venv --python 3.12 && uv pip install -r requirements.txt && streamlit run app.py`

**Kapsam:** NBA tarihi verisini interaktif olarak keşfeden kısa bir takım egzersizi, üretim ortamı için bir dashboard değil.

</details>

---

A team project by Nurettin Macit, Mehmet Arda Öncel, and Yusuf Oğuz. An interactive Streamlit dashboard covering 77 years of NBA history, a real deployable app rather than a set of static notebook charts.

**Scope:** an interactive exploration of NBA history data, built as a short team exercise rather than a production dashboard.

## What it does

Five tabs, each covering a different angle on the data:

| Tab | What's in it |
|---|---|
| Three-Point Revolution | How the three-point shot evolved across NBA history |
| Physical vs Performance | How physical traits (height, weight) relate to performance |
| Career Arc & Peak Age | Player career curves and the age they peak at |
| Geography | Where players were born, a country-level world map plus an interactive US state-level choropleth built with Plotly |
| Position Profiles | Statistical profile comparisons by position |

## Data

21 separate CSV files under `data/`, sourced from Basketball Reference: per-game, per-100-possession, and play-by-play stats for individual players, team stats, draft history, award voting, All-Star selections. Player birthplaces and player profile data are processed as their own separate datasets.

## Architecture

```
datavizprop/
├── app.py                  Streamlit entry point, wires up the 5 tabs
├── data_loader.py           Data loading and caching layer
├── tabs/                    Each tab is its own module with a render() function
│   ├── tab_threept.py
│   ├── tab_physical.py
│   ├── tab_career.py
│   ├── tab_geo.py
│   └── tab_positions.py
├── data/, data_birthplaces/, data_players/    Raw CSV data
├── figures/                 Static figures generated for the report and presentation
├── report.pdf / report.tex   Written project report (IEEE conference paper format)
├── presentation.pptx         Slide deck
├── demo_day_guide.html       Presenter's cue sheet for the live demo
└── Project Proposal.pdf      The original project proposal
```

## Running it

```bash
cd datavizprop
uv venv --python 3.12 && uv pip install -r requirements.txt
streamlit run app.py
```

## Tools

Streamlit for the app itself, Plotly for the interactive maps and charts, Pandas and NumPy for data handling, Matplotlib/Seaborn/Statsmodels for the static analysis in the written report.
