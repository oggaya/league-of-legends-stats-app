import pandas as pd

def prepare_dataframe(rows):
    """Convertit les données brutes en DataFrame et ajoute les métriques de base."""
    df = pd.DataFrame(rows)
    
    # Écarter les remakes
    df = df[df["duration_min"] > 5].copy()
    
    # Calcul des colonnes dérivées
    df["kda"] = (df["kills"] + df["assists"]) / df["deaths"].clip(lower=1)
    df["cs_min"] = df["cs"] / df["duration_min"]
    df["morts_min"] = df["deaths"] / df["duration_min"] 
    df["dmg_min"] = df["damage"] / df["duration_min"]
    
    return df

def get_champion_stats(df, min_games):
    """Agrège les statistiques par champion."""
    stats = (
        df.groupby("champion")
        .agg(
            parties=("win", "size"),
            winrate=("win", "mean"),
            kda=("kda", "mean"),
            morts=("deaths", "mean"),
            cs_min=("cs_min", "mean"),
            degats=("damage", "mean"),
        )
        .sort_values("parties", ascending=False)
        .round(2)
    )
    return stats[stats["parties"] >= min_games]

def get_win_loss_metrics(df):
    """Compare les statistiques moyennes entre les victoires et les défaites."""
    return (
        df.groupby("win")
        .agg(
            parties=("win", "size"),
            morts=("deaths", "mean"),
            morts_min=("morts_min", "mean"),
            kda=("kda", "mean"),
            cs_min=("cs_min", "mean"),
            degats=("damage", "mean"),
            duree=("duration_min", "mean"),
            degats_min=("dmg_min", "mean"),
        )
        .round(2)
    )