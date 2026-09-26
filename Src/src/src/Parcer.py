import re
import pandas as pd
from typing import Union
import io

VALUE_TAGS = {"STRONG VALUE", "VALUE"}

POSITIONS = {"QB", "RB", "WR", "TE", "DEF", "K"}

# FanDuel uses some non-standard abbreviations
TEAM_NORMALIZE = {
    "San Diego Chargers": "LAC",
    "Washington Redskins": "WAS",
    "Las Vegas Raiders": "LV",
    "Los Angeles Rams": "LAR",
    "Los Angeles Chargers": "LAC",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "San Francisco 49ers": "SF",
    "Tampa Bay Buccaneers": "TB",
    "New Orleans Saints": "NO",
    "Carolina Panthers": "CAR",
    "Pittsburgh Steelers": "PIT",
    "Houston Texans": "HOU",
    "Buffalo Bills": "BUF",
    "Detroit Lions": "DET",
    "Kansas City Chiefs": "KC",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "Seattle Seahawks": "SEA",
    "Indianapolis Colts": "IND",
    "Dallas Cowboys": "DAL",
    "Tennessee Titans": "TEN",
    "Baltimore Ravens": "BAL",
    "Cleveland Browns": "CLE",
    "Cincinnati Bengals": "CIN",
    "Arizona Cardinals": "ARI",
    "Miami Dolphins": "MIA",
    "Philadelphia Eagles": "PHI",
    "Chicago Bears": "CHI",
    "Denver Broncos": "DEN",
    "Atlanta Falcons": "ATL",
    "Green Bay Packers": "GB",
    "Jacksonville Jaguars": "JAX",
    "Washington Commanders": "WAS",
}


def _clean_salary(s: str) -> int:
    return int(re.sub(r"[^0-9]", "", s))


def _clean_proj(s: str) -> float:
    return float(re.sub(r"[^0-9.]", "", s))


def parse_fanduel_file(file: Union[io.IOBase, str]) -> pd.DataFrame:
    if hasattr(file, "read"):
        raw = file.read().decode("utf-8", errors="ignore")
    else:
        raw = file

    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    # Drop header
    if lines and lines[0].upper().startswith("PLAYER"):
        lines = lines[1:]

    records = []
    buf = []  # accumulate tokens between records

    # We detect a record by finding the salary token ($X,XXX).
    # Everything before it is name + optional tag.
    # Everything after it is team... wait — team comes before salary.
    # Real order: NAME, [tag], POS, TEAM, SALARY, PROJ
    # We'll scan forward for SALARY, then look back for POS + TEAM.

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Salary token?
        if line.startswith("$"):
            salary = _clean_salary(line)
            # Proj is next line
            proj = _clean_proj(lines[i + 1]) if i + 1 < n else 0.0

            # Walk backwards to find POS and TEAM
            pos = None
            team = None
            name_parts = []
            j = i - 1
            while j >= 0:
                tok = lines[j]
                if tok in POSITIONS and pos is None:
                    pos = tok
                elif pos is not None and team is None and re.fullmatch(r"[A-Z]{2,3}", tok):
                    team = tok
                    break
                elif tok in VALUE_TAGS:
                    pass
                elif re.fullmatch(r"\d+\.\d+", tok):
                    # This is a value score like 2.77 — skip
                    pass
                else:
                    name_parts.insert(0, tok)
                j -= 1

            if pos and team and name_parts:
                name = " ".join(name_parts).strip()
                # Normalize DEF names
                if pos == "DEF" and name in TEAM_NORMALIZE:
                    team = TEAM_NORMALIZE[name]
                    name = name  # keep full name for display
                records.append({
                    "PLAYER": name,
                    "POS": pos,
                    "TEAM": team,
                    "SALARY": salary,
                    "PROJ": proj,
                })

            i += 2
            continue

        i += 1

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError("No players parsed from file.")

    # Dedup — keep first occurrence
    df = df.drop_duplicates(subset=["PLAYER", "TEAM"], keep="first").reset_index(drop=True)

    return df
