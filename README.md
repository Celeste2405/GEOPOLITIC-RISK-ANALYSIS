# GeoRisk Credit Overlay
### From Geopolitical Risk to Credit Risk: A Macroeconomic Stress Testing Framework

## 1. Présentation du projet

Les tensions géopolitiques peuvent affecter la stabilité économique et financière à travers plusieurs canaux : perturbations commerciales, hausse des prix de l'énergie, inflation, ralentissement de l'activité ou volatilité des marchés financiers. Ces chocs peuvent ensuite fragiliser la situation financière des entreprises et accroître leur risque de défaut.

**GeoRisk Credit Overlay** est un projet de Data Science et de modélisation du risque de crédit visant à étudier comment les variations du risque géopolitique peuvent se transmettre aux conditions macroéconomiques, puis aux probabilités de défaut (*Probability of Default – PD*) d'un portefeuille de crédit.

Le projet s'appuie sur les indicateurs **AI-GPR (Artificial Intelligence Geopolitical Risk)** développés par Iacoviello et Tong (2026), qui utilisent des modèles de langage pour mesurer l'intensité et la nature des risques géopolitiques à partir d'articles de presse.

L'objectif final est de construire un cadre quantitatif permettant de simuler des scénarios de tensions géopolitiques et d'évaluer leurs conséquences potentielles sur le risque de crédit bancaire.

## 2. Objectifs

Le projet poursuit quatre objectifs principaux :

1. **Mesurer le risque géopolitique** à partir des indices AI-GPR, en distinguant les risques globaux, nationaux, bilatéraux et énergétiques.
2. **Analyser les mécanismes de transmission macroéconomique** entre les tensions géopolitiques et des variables telles que le PIB, l'inflation, les taux d'intérêt ou les échanges commerciaux.
3. **Quantifier les impacts potentiels sur le risque de crédit**, notamment sur les probabilités de défaut et les pertes de crédit attendues.
4. **Développer un outil interactif de stress testing** permettant de visualiser les scénarios, les résultats des modèles et les sensibilités du portefeuille.

## 3. Référence scientifique : l'indice AI-GPR

Le projet s'inspire de l'article :

**Iacoviello, M. & Tong, J. (2026). *The AI-GPR Index: Measuring Geopolitical Risk using Artificial Intelligence*.**

Les auteurs proposent une nouvelle mesure du risque géopolitique fondée sur l'analyse automatisée d'environ 4,6 millions d'articles de presse publiés depuis 1960 dans trois journaux américains : *New York Times*, *Washington Post* et *Chicago Tribune*.

### 3.1. Méthodologie des auteurs

La construction de l'indice repose sur deux étapes :

- **Filtrage par mots-clés** : sélection des articles susceptibles de contenir des informations géopolitiques.
- **Classification par LLM** : utilisation de GPT-4o mini pour attribuer à chaque article un score de risque géopolitique compris entre 0 et 1.

Les scores sont ensuite agrégés quotidiennement, rapportés au volume total d'articles publiés, puis normalisés sur la période 1985–2019.

Cette approche permet de dépasser certaines limites des indices traditionnels fondés uniquement sur des mots-clés, notamment en tenant compte du contexte et de l'intensité des événements.

### 3.2. Indicateurs disponibles

| Indicateur | Description |
|---|---|
| AI-GPR | Intensité globale du risque géopolitique |
| Threats GPR | Risques associés aux menaces géopolitiques |
| Acts GPR | Risques associés aux événements effectivement survenus |
| Country GPR | Risque géopolitique associé à un pays |
| Bilateral GPR | Risque géopolitique entre deux pays |
| Oil GPR | Risque de perturbation géopolitique de l'approvisionnement pétrolier |

**Données et documentation :** https://www.matteoiacoviello.com/ai_gpr.html

## 4. Collecte des données

### 4.1. Périmètre de l'étude

L'étude porte initialement sur cinq pays :

- France (`FRA`)
- Allemagne (`DEU`)
- Italie (`ITA`)
- Espagne (`ESP`)
- États-Unis (`USA`)

La période cible est **2000–2025**, sous réserve de disponibilité des données pour chaque source.

Les données proviennent de plusieurs bases publiques et sont collectées à leurs fréquences d'origine avant harmonisation.

### 4.2. Données géopolitiques — AI-GPR

Les données géopolitiques proviennent des indices **AI-GPR (Artificial Intelligence Geopolitical Risk)** développés par Iacoviello et Tong (2026). Ces indicateurs mesurent l'intensité des tensions géopolitiques à partir de l'analyse automatisée d'articles de presse par des modèles de langage.

**Source :** [AI-GPR — Iacoviello & Tong](https://www.matteoiacoviello.com/ai_gpr.html)

**Fréquence :** mensuelle.

**Couverture temporelle :** à partir de janvier 1960.

**Périmètre géographique :** 200 pays.

**Période retenue pour l'étude :** janvier 2000 – décembre 2025.

#### Variables collectées

La base comprend un indice global de risque géopolitique (`GPR_AI`) ainsi que quatre indicateurs pour chaque pays :

| Indicateur | Description |
|---|---|
| `GPR_AI` | Indice global de risque géopolitique |
| `all` | Risque géopolitique total associé au pays |
| `initiator` | Risque lié aux événements géopolitiques dans lesquels le pays joue un rôle d'initiateur |
| `respondent` | Risque lié aux événements géopolitiques auxquels le pays répond |
| `spillover` | Risque lié aux répercussions indirectes des événements géopolitiques sur le pays |

Ces données permettent de distinguer les tensions géopolitiques mondiales des risques associés à chaque pays, et d'étudier leurs relations avec les conditions macroéconomiques et financières.

### 4.3. Données macroéconomiques — Banque mondiale

Les données macroéconomiques sont utilisées pour étudier les mécanismes de transmission des chocs géopolitiques à l'activité économique et, à terme, au risque de crédit.

**Source :** [Banque mondiale — World Development Indicators (WDI)](https://data.worldbank.org/)

**Période :** 2000–2025.

**Fréquence :** annuelle.

| Variable | Code Banque mondiale | Description |
|---|---|---|
| Croissance du PIB réel | `NY.GDP.MKTP.KD.ZG` | Croissance annuelle du PIB réel (%) |
| Inflation | `FP.CPI.TOTL.ZG` | Variation annuelle de l'indice des prix à la consommation (%) |
| Taux de chômage | `SL.UEM.TOTL.ZS` | Part de la population active au chômage (%) |
| Ouverture commerciale | `NE.TRD.GNFS.ZS` | Somme des exportations et importations en pourcentage du PIB |

Les données ont été récupérées automatiquement via l'API REST de la Banque mondiale.

### 4.4. Données financières et monétaires — FRED

Les données financières et monétaires permettent d'étudier les effets des tensions géopolitiques sur les conditions de financement, les marchés obligataires et les prix de l'énergie.

**Source :** [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)

**Période :** janvier 2000 – décembre 2025.

**Fréquence :** quotidienne ou mensuelle selon les séries.

| Variable | Code FRED | Description |
|---|---|---|
| Taux effectif des fonds fédéraux | `FEDFUNDS` | Taux effectif des fonds fédéraux américains (%) |
| Taux de la facilité de dépôt BCE | `ECBDFR` | Taux de référence de la politique monétaire de la zone euro (%) |
| Prix du pétrole Brent | `DCOILBRENTEU` | Prix du baril de Brent en USD |
| Prix du pétrole WTI | `DCOILWTICO` | Prix du baril de WTI en USD |
| Rendement souverain à 10 ans — France | `IRLTLT01FRM156N` | Rendement des obligations d'État françaises (%) |
| Rendement souverain à 10 ans — Allemagne | `IRLTLT01DEM156N` | Rendement des obligations d'État allemandes (%) |
| Rendement souverain à 10 ans — Italie | `IRLTLT01ITM156N` | Rendement des obligations d'État italiennes (%) |
| Rendement souverain à 10 ans — Espagne | `IRLTLT01ESM156N` | Rendement des obligations d'État espagnoles (%) |
| Rendement souverain à 10 ans — États-Unis | `IRLTLT01USM156N` | Rendement des obligations d'État américaines (%) |

Les données ont été téléchargées automatiquement depuis les fichiers CSV publics de FRED.

### 4.5. Primes de risque pays et actions — Damodaran

Les données d'Aswath Damodaran (NYU Stern) complètent les indicateurs financiers par des estimations du risque pays et des primes de risque exigées par les investisseurs sur les marchés actions.

**Source :** [Damodaran — Country Risk Premiums](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html)

**Millésime collecté :** janvier 2026.

**Fréquence :** photographie ponctuelle ; les archives annuelles restent à collecter.

| Variable | Description |
|---|---|
| `sovereign_rating` | Notation souveraine Moody's |
| `default_spread` | Spread de défaut souverain estimé à partir de la notation |
| `country_risk_premium` | Prime de risque additionnelle associée au pays |
| `equity_risk_premium` | Prime de risque actions totale estimée pour le pays |

Les primes de risque actions sont construites à partir d'une prime de référence pour les marchés matures, à laquelle s'ajoute une prime spécifique au pays.

Ces données permettront de comparer les estimations de risque pays aux indicateurs géopolitiques AI-GPR et aux spreads souverains observés.

## 5. Prétraitement et construction des variables

Cette étape vise à nettoyer, harmoniser et enrichir les données collectées afin de constituer des bases exploitables pour l'analyse statistique et la modélisation économétrique.
### 5.1. Données géopolitiques — AI-GPR

Les indices AI-GPR nationaux ont été extraits du fichier mensuel des auteurs afin de construire un panel géographique sur la période **janvier 2000 – décembre 2025**.

Les opérations réalisées comprennent :

- Sélection des cinq pays étudiés : France, Allemagne, Italie, Espagne et États-Unis.
- Extraction des quatre composantes nationales : `all`, `initiator`, `respondent` et `spillover`.
- Harmonisation des identifiants géographiques au format ISO3.
- Conversion des dates et des valeurs numériques.
- Restructuration des données du format large vers un panel pays × mois.
- Intégration de l'indice global `GPR_AI` comme facteur commun aux cinq pays.

**Contrôle de qualité**

La base finale contient **1 560 observations et 7 colonnes**, correspondant à 312 observations mensuelles pour chacun des cinq pays, sur la période 2000–2025.

Aucune valeur manquante n'a été détectée.

**Fichier produit :** `data/processed/ai_gpr_country_monthly.csv`

Les séries nationales et l'indice global seront utilisés pour étudier les relations entre les tensions géopolitiques et l'évolution des conditions économiques et financières.

### 5.2. Données macroéconomiques — Banque mondiale

Les données des quatre indicateurs ont été regroupées dans une table unique structurée par pays et par année.

Les opérations réalisées comprennent :

- Harmonisation des identifiants pays au format ISO3.
- Fusion des indicateurs sur les clés `country` et `year`.
- Tri chronologique des observations.

La base annuelle sera intégrée aux autres sources après définition de la fréquence commune de modélisation.

### 5.2. Données financières et monétaires — FRED

Les séries collectées ont été harmonisées à fréquence mensuelle. Les observations quotidiennes ont été agrégées par moyenne mensuelle.

Deux catégories d'indicateurs supplémentaires ont été construites.

**Spreads souverains à 10 ans**

Pour la France, l'Italie et l'Espagne, les spreads sont calculés par rapport au rendement souverain allemand à 10 ans, utilisé comme référence pour les pays de la zone euro :


$$
\text{Spread}_{i,t}^{10Y} = \text{Yield}_{i,t}^{10Y} - \text{Yield}_{DE,t}^{10Y}
$$

Les spreads sont exprimés en points de pourcentage.

**Variations annuelles des prix du pétrole**

Pour le Brent et le WTI, les variations en glissement annuel sont calculées selon :

$$
\Delta \text{Oil}_{t}^{YoY} = \left(\frac{P_t}{P_{t-12}} - 1\right) \times 100
$$

Ces variables permettent de mesurer l'évolution des prix de l'énergie sur douze mois.

**Contrôle de qualité**

La base consolidée contient **312 observations mensuelles et 14 variables**, dont neuf séries collectées et cinq indicateurs dérivés.

- Les neuf séries collectées sont complètes sur la période étudiée.
- Les trois spreads souverains calculés ne présentent aucune valeur manquante.
- Les variations annuelles du Brent et du WTI présentent chacune 12 valeurs manquantes initiales, liées au calcul sur douze mois.
- Aucune autre valeur manquante n'a été détectée.

### 5.3. Primes de risque pays — Damodaran

Les données ont été extraites de la feuille `ERPs by country` du classeur Excel de Damodaran.

Les opérations réalisées comprennent :

- Sélection des cinq pays étudiés.
- Extraction des notations souveraines et des primes fondées sur les notations.
- Harmonisation des noms de pays selon les codes ISO3.
- Conservation des valeurs financières au format décimal.
- Ajout de la date du millésime (`snapshot_date`).

La base finale contient **5 observations et 6 colonnes**, sans aucune valeur manquante.

Les valeurs de janvier 2026 sont conservées séparément des données historiques afin d'éviter toute utilisation d'informations futures dans les analyses portant sur 2000–2025.

### 5.4. Harmonisation des sources et constitution du dataset final

*Étape à réaliser.*

Cette étape consistera à :

- Définir une fréquence commune d'analyse.
- Harmoniser les identifiants géographiques et les périodes.
- Intégrer les indices AI-GPR.
- Examiner les valeurs manquantes et les différences de couverture temporelle.
- Construire une base consolidée pour la modélisation.

## 6. Organisation des données

Les fichiers sont organisés selon leur niveau de transformation :

```text
data/
├── raw/
│   ├── fred_daily_monthly.csv
│   └── damodaran_ctryprem.xlsx
│
└── processed/
    ├── fred_monthly.csv
    └── damodaran_country_risk_2026.csv
```

Les fichiers de la Banque mondiale et les futurs fichiers AI-GPR pourront être ajoutés à cette arborescence au fur et à mesure de leur intégration.

## 7. Analyse exploratoire du risque géopolitique

Une analyse exploratoire des indices AI-GPR nationaux a été réalisée sur la période **2000–2025** pour cinq pays : France, Allemagne, Italie, Espagne et États-Unis. Elle comprend l'étude des distributions, la comparaison des séries brutes et standardisées, l'identification des mois de risque extrême (au-delà du 95e percentile national) et l'analyse des composantes *initiator*, *respondent* et *spillover*.

Les résultats mettent en évidence une forte hétérogénéité entre les pays. Les effets de *spillover* représentent la composante majoritaire en Allemagne (63,3 %), en France (57,1 %) et en Italie (53,7 %), tandis que le rôle d'initiateur prédomine aux États-Unis (55,7 %). La composition du risque varie également lors des épisodes extrêmes.

**Notebook :** `notebooks/01_exploratory_data_analysis.ipynb`

## 8. Construction du panel géopolitique et financier

Les données AI-GPR mensuelles ont été fusionnées avec les séries financières de FRED sur la période **janvier 2000 – décembre 2025**, afin de constituer un panel de **1 560 observations (5 pays × 312 mois) et 24 colonnes**. Il rassemble les indices géopolitiques nationaux et globaux, les rendements souverains à 10 ans, les spreads par rapport à l'Allemagne, les taux directeurs de la BCE et de la Fed, ainsi que les prix du Brent et du WTI et leurs variations annuelles.

Les contrôles ont confirmé l'absence de doublons et la disponibilité des principales variables financières. Les valeurs manquantes restantes sont structurelles : spreads non définis pour les États-Unis et variations annuelles du pétrole indisponibles sur les douze premiers mois.

**Script :** `src/build_financial_panel.py`  
**Base produite :** `data/processed/georisk_financial_panel.csv`


















## 8. Modélisation de la transmission macroéconomique

*À venir.*

## 9. Modélisation du risque de crédit et stress testing

*À venir.*

## 10. Dashboard interactif

*À venir.*
