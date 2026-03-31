# 📈 CAPM / MEDAF — Attijariwafa Bank vs MASI

<img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python" /><img src="https://img.shields.io/badge/Statsmodels-OLS%20Regression-orange" alt="Statsmodels" /><img src="https://img.shields.io/badge/License-MIT-green" alt="License" /><img src="https://img.shields.io/badge/Status-Complete-brightgreen" alt="Status" />> **Capital Asset Pricing Model (MEDAF)** — Estimation du risque systématique (β) de l'action **Attijariwafa Bank (ATR)** sur la Bourse de Casablanca, avec validation économétrique complète des hypothèses de Gauss-Markov.

---

## 🎯 Objectifs

| \# | Objectif |
| --- | --- |
| 1 | Calculer les **rendements log-normaux** quotidiens de ATR et du MASI |
| 2 | Estimer **β (bêta systématique)** et **α (alpha de Jensen)** par régression MCO |
| 3 | Valider les hypothèses OLS : normalité, homoscédasticité, absence d'autocorrélation |
| 4 | Décomposer la variance en **risque systématique** et **risque idiosyncratique** |
| 5 | Calculer les métriques de performance : Sharpe, Treynor, Information Ratio |

---

## 🧮 Modèle Théorique

Le CAPM (Sharpe, 1964 ; Lintner, 1965) spécifie :

$$R\_{i,t} - R_f = \\alpha_i + \\beta_i \\underbrace{(R\_{m,t} - R_f)}*{\\text{prime de risque marché}} + \\varepsilon*{i,t}$$

avec $\\varepsilon\_{i,t} \\sim \\mathcal{N}(0, \\sigma^2)$ et $\\mathbb{E}\[\\varepsilon\_{i,t} \\cdot R\_{m,t}\] = 0$.

La décomposition du risque donne :

$$\\underbrace{\\text{Var}(R_i)}*{\\text{risque total}} = \\underbrace{\\beta_i^2 \\cdot \\text{Var}(R_m)}*{\\text{systématique}} + \\underbrace{\\text{Var}(\\varepsilon_i)}\_{\\text{spécifique}}$$

---

## 📊 Résultats Clés *(à mettre à jour après exécution)*

| Paramètre | Valeur | Interprétation |
| --- | --- | --- |
| **β (Bêta)** | `~1.1390` | ATR est **défensive** — moins volatile que le marché |
| **α (Alpha)** | `~-0.000066` | Performance anormale nulle (H₀: α=0 non rejetée) |
| **R²** | `~0.4085` | 41% de la variance d'ATR expliquée par le MASI |
---

## 🗂️ Structure du Projet

```
CAPM-Morocco-Market-Analysis/
│
├── 📁 data/                    # Données brutes (Investing.com)
│   ├── ATR.csv                # Prix quotidiens Attijariwafa Bank
│   └── MASI.csv               # Indice MASI (Moroccan All Shares Index)
│
├── 📁 src/                     # Module Python réutilisable
│   ├── __init__.py
│   └── utils.py                # Nettoyage données, calcul rendements, métriques
│
├── 📁 notebooks/               # Analyse principale
│   └── CAPM_Analysis.ipynb     # Notebook structuré (EDA → OLS → Tests → Risque)
│
├── 📁 outputs/                 # Figures générées automatiquement
│   ├── eda_overview.png
│   ├── capm_sml.png
│   └── residual_diagnostics.png
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Tests Économétriques Implémentés

| Test | Hypothèse vérifiée | Package |
| --- | --- | --- |
| **Jarque-Bera** | Normalité des résidus | `scipy.stats` |
| **Shapiro-Wilk** | Normalité (échantillons &lt; 5000) | `scipy.stats` |
| **Durbin-Watson** | Absence d'autocorrélation (lag 1) | `statsmodels` |
| **Ljung-Box** | Absence d'autocorrélation (lags 5, 10, 20) | `statsmodels` |
| **Breusch-Pagan** | Homoscédasticité | `statsmodels` |
| **ACF des résidus²** | Absence d'effet ARCH (volatilité conditionnelle) | `statsmodels` |

---

## 🚀 Installation & Exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/CAPM-Morocco-Market-Analysis.git
cd CAPM-Morocco-Market-Analysis
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Placer les données

Télécharger les données historiques depuis [Investing.com](https://investing.com) :

- **ATR** : Attijariwafa Bank → Données historiques → Exporter `.csv`
- **MASI** : MASI Index → Données historiques → Exporter `.csv`

Placer les fichiers dans `data/`.

### 4. Lancer le notebook

```bash
jupyter notebook notebooks/CAPM_Analysis.ipynb
```

---

## 🛠️ Stack Technique

| Bibliothèque | Usage |
| --- | --- |
| `pandas` | Manipulation et fusion des séries temporelles |
| `numpy` | Calculs vectorisés (rendements, variance) |
| `statsmodels` | Régression OLS, tests d'autocorrélation et d'hétéroscédasticité |
| `scipy` | Tests de normalité (JB, Shapiro-Wilk), Q-Q plot |
| `matplotlib` | Visualisations (SML, diagnostics de résidus) |

---

## 📚 Références

- Sharpe, W.F. (1964). *Capital asset prices: A theory of market equilibrium under conditions of risk.* Journal of Finance.
- Lintner, J. (1965). *The valuation of risk assets and the selection of risky investments.* Review of Economics and Statistics.
- Fama, E.F. & French, K.R. (1992). *The cross-section of expected stock returns.* Journal of Finance.

---

## 👤 Auteur

**Mohamed El Otmany**\
Étudiant Ingénieur 2ème année — Finance & Actuariat\
FST Errachidia, Université Moulay Ismail

<img src="https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin" alt="LinkedIn" /><img src="https://img.shields.io/badge/GitHub-Follow-black?logo=github" alt="GitHub" />---

*Ce projet a été réalisé dans le cadre d'une analyse quantitative des marchés financiers marocains.*
