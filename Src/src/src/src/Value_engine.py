import pandas as pd
import numpy as np


# GPP weights — ceiling-heavy
WEIGHTS = {
    "CEILING_SCORE": 0.35,
    "LEVERAGE": 0.25,
    "VALUE": 0.20,
    "MATCHUP": 0.15,
    "FLOOR_SCORE": 0.05,
}


def _estimate_ownership(df: pd.DataFrame) -> pd.Series:
    """
    Rough ownership estimate until we wire real ownership scraping.
    Higher proj + higher salary → higher ownership.
    """
    proj_rank = df["PROJ"].rank(pct=True)
    sal_rank = df["SALARY"].rank(pct=True)
    raw = 0.6 * proj_rank + 0.4 * sal_rank
    # Scale to 1–40% range
    return (1 + raw * 39).round(1)


def _ceiling(proj: pd.Series) -> pd.Series:
    # Placeholder until XGBoost quantile model is wired in Step 3.
    # FanDuel proj × 1.35 approximates a 90th percentile ceiling.
    return (proj * 1.35).round(1)


def _floor(proj: pd.Series) -> pd.Series:
    # Placeholder — 25th percentile approximation.
    return (proj * 0.65).round(1)


def _matchup_grade(df: pd.DataFrame) -> pd.Series:
    # Placeholder — will pull DVOA in Step 3.
    # Neutral 50 grade until then.
    return pd.Series([50.0] * len(df), index=df.index)


def compute_value_rankings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["SALARY_K"] = df["SALARY"] / 1000.0
    df["VALUE"] = (df["PROJ"] / df["SALARY_K"]).round(2)
    df["CEILING"] = _ceiling(df["PROJ"])
    df["FLOOR"] = _floor(df["PROJ"])
    df["OWNERSHIP"] = _estimate_ownership(df)
    df["LEVERAGE"] = (df["PROJ"] / df["OWNERSHIP"]).round(2)
    df["CEILING_SCORE"] = (df["CEILING"] / df["SALARY_K"]).round(2)
    df["FLOOR_SCORE"] = (df["FLOOR"] / df["SALARY_K"]).round(2)
    df["MATCHUP"] = _matchup_grade(df)

    # Normalize each component to 0–100 scale for composite blending
    def norm(s):
        s_min, s_max = s.min(), s.max()
        if s_max == s_min:
            return pd.Series([50.0] * len(s), index=s.index)
        return ((s - s_min) / (s_max - s_min) * 100).round(2)

    df["CEILING_NORM"] = norm(df["CEILING_SCORE"])
    df["LEVERAGE_NORM"] = norm(df["LEVERAGE"])
    df["VALUE_NORM"] = norm(df["VALUE"])
    df["MATCHUP_NORM"] = df["MATCHUP"]  # already 0–100
    df["FLOOR_NORM"] = norm(df["FLOOR_SCORE"])

    df["COMPOSITE"] = (
        WEIGHTS["CEILING_SCORE"] * df["CEILING_NORM"]
        + WEIGHTS["LEVERAGE"] * df["LEVERAGE_NORM"]
        + WEIGHTS["VALUE"] * df["VALUE_NORM"]
        + WEIGHTS["MATCHUP"] * df["MATCHUP_NORM"]
        + WEIGHTS["FLOOR_SCORE"] * df["FLOOR_NORM"]
    ).round(2)

    return df
