"""
utils.py — CAPM Morocco Market Analysis
========================================
Auteur : Mohamed El Otmany
FST Errachidia — Génie Financier & Actuariat

Fonctions utilitaires pour :
    - Nettoyage des exports Investing.com (.xlsx / .csv)
    - Calcul des rendements log-normaux
    - Statistiques descriptives financières
"""

import pandas as pd
import numpy as np
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# 1. CHARGEMENT & NETTOYAGE DES DONNÉES INVESTING.COM
# ──────────────────────────────────────────────────────────────────────────────

def clean_investing_data(filepath: str, price_col: str = "Price") -> pd.DataFrame:
    """
    Charge et nettoie un fichier exporté depuis Investing.com.

    Gère les cas suivants :
        - Prix au format string avec virgules : "1,200.50" → 1200.50
        - Dates au format DD/MM/YYYY ou YYYY-MM-DD
        - Colonnes supplémentaires (Vol., Change %) ignorées

    Parameters
    ----------
    filepath   : str  — Chemin vers le fichier (.xlsx ou .csv)
    price_col  : str  — Nom de la colonne de prix (défaut : "Price")

    Returns
    -------
    pd.DataFrame avec colonnes ['Date', 'Price'], triée par date croissante.
    """
    ext = filepath.split(".")[-1].lower()

    if ext == "xlsx":
        df = pd.read_excel(filepath)
    elif ext == "csv":
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f"Format non supporté : .{ext}. Utilisez .xlsx ou .csv.")

    # Vérification colonnes
    if "Date" not in df.columns or price_col not in df.columns:
        raise KeyError(
            f"Colonnes attendues : ['Date', '{price_col}']. "
            f"Colonnes trouvées : {list(df.columns)}"
        )

    df = df[["Date", price_col]].copy()

    # Nettoyage prix : "1,200.50" → 1200.50
    df[price_col] = (
        df[price_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")

    # Parsing dates (Investing.com utilise souvent JJ/MM/AAAA)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Suppression valeurs manquantes
    n_before = len(df)
    df = df.dropna(subset=["Date", price_col])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        print(f"  [clean_investing_data] {n_dropped} ligne(s) supprimée(s) (NaN).")

    # Tri chronologique
    df = df.sort_values("Date").reset_index(drop=True)

    # Renommage standardisé
    df = df.rename(columns={price_col: "Price"})

    return df


# ──────────────────────────────────────────────────────────────────────────────
# 2. CALCUL DES RENDEMENTS
# ──────────────────────────────────────────────────────────────────────────────

def calculate_log_returns(series: pd.Series) -> pd.Series:
    """
    Calcule les rendements log-normaux : r_t = ln(P_t / P_{t-1}).

    Préféré aux rendements arithmétiques pour les propriétés d'additivité
    temporelle et la robustesse aux grandes variations.

    Parameters
    ----------
    series : pd.Series — Série de prix

    Returns
    -------
    pd.Series des rendements logarithmiques (premier élément = NaN).
    """
    return np.log(series / series.shift(1))


def calculate_arithmetic_returns(series: pd.Series) -> pd.Series:
    """
    Calcule les rendements arithmétiques : r_t = (P_t - P_{t-1}) / P_{t-1}.
    """
    return series.pct_change()


# ──────────────────────────────────────────────────────────────────────────────
# 3. STATISTIQUES FINANCIÈRES
# ──────────────────────────────────────────────────────────────────────────────

def annualize_return(daily_return: float, trading_days: int = 252) -> float:
    """Annualise un rendement quotidien moyen."""
    return (1 + daily_return) ** trading_days - 1


def annualize_volatility(daily_vol: float, trading_days: int = 252) -> float:
    """Annualise une volatilité quotidienne."""
    return daily_vol * np.sqrt(trading_days)


def sharpe_ratio(
    returns: pd.Series,
    rf_annual: float = 0.035,
    trading_days: int = 252
) -> float:
    """
    Calcule le ratio de Sharpe annualisé.

    Parameters
    ----------
    returns      : pd.Series — Rendements quotidiens
    rf_annual    : float     — Taux sans risque annuel (défaut : 3.5% — BdT Maroc)
    trading_days : int       — Jours de bourse par an

    Returns
    -------
    float — Ratio de Sharpe
    """
    rf_daily    = rf_annual / trading_days
    excess_ret  = returns - rf_daily
    ann_excess  = excess_ret.mean() * trading_days
    ann_vol     = returns.std() * np.sqrt(trading_days)
    return ann_excess / ann_vol if ann_vol > 0 else np.nan


def compute_capm_metrics(
    r_stock: pd.Series,
    r_market: pd.Series,
    rf_annual: float = 0.035,
    trading_days: int = 252
) -> dict:
    """
    Calcule les métriques CAPM principales sans régression (méthode covariante).

    Beta = Cov(R_i, R_m) / Var(R_m)
    Alpha = E[R_i] - Beta * E[R_m]

    Parameters
    ----------
    r_stock   : rendements actif
    r_market  : rendements marché
    rf_annual : taux sans risque annuel
    trading_days : jours de bourse

    Returns
    -------
    dict avec beta, alpha, correlation, treynor_ratio, information_ratio
    """
    cov_matrix = np.cov(r_stock.dropna(), r_market.dropna())
    beta  = cov_matrix[0, 1] / cov_matrix[1, 1]
    alpha = r_stock.mean() - beta * r_market.mean()
    corr  = np.corrcoef(r_stock.dropna(), r_market.dropna())[0, 1]

    rf_daily = rf_annual / trading_days
    treynor  = (r_stock.mean() * trading_days - rf_annual) / beta if beta != 0 else np.nan

    # Tracking error (écart-type de l'excès de rendement vs marché)
    active_return   = r_stock - r_market
    tracking_error  = active_return.std() * np.sqrt(trading_days)
    info_ratio = (active_return.mean() * trading_days) / tracking_error if tracking_error > 0 else np.nan

    return {
        "beta"             : round(beta,  6),
        "alpha_daily"      : round(alpha, 8),
        "alpha_annualized" : round(alpha * trading_days, 6),
        "correlation"      : round(corr,  6),
        "treynor_ratio"    : round(treynor, 6),
        "information_ratio": round(info_ratio, 6),
        "tracking_error"   : round(tracking_error, 6),
    }


def print_summary_table(metrics: dict) -> None:
    """Affiche un tableau récapitulatif des métriques CAPM."""
    print("\n" + "=" * 50)
    print("       MÉTRIQUES CAPM — RÉSUMÉ")
    print("=" * 50)
    for key, val in metrics.items():
        print(f"  {key:<22} : {val}")
    print("=" * 50 + "\n")
