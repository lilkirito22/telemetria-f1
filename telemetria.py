import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def buscar_dados_volta(driver, session_key):
    url = f"https://api.openf1.org/v1/car_data?driver_number={driver}&session_key={session_key}"
    response = requests.get(url)
    dados = response.json()
    return pd.DataFrame(dados)


def buscar_voltas(driver, session_key):
    url = f"https://api.openf1.org/v1/laps?driver_number={driver}&session_key={session_key}"
    response = requests.get(url)
    dados = response.json()
    return pd.DataFrame(dados)


def buscar_melhor_volta(df_voltas):
    df = df_voltas.dropna(subset=["lap_duration"]).copy()
    melhor = df.loc[df["lap_duration"].idxmin()]
    return melhor


def filtrar_volta(df_telemetria, best_lap):
    inicio = pd.to_datetime(best_lap["date_start"], format="mixed")
    fim = inicio + pd.to_timedelta(best_lap["lap_duration"], unit="s")
    df_filtrado = df_telemetria[
        (df_telemetria["date"] >= inicio) & (df_telemetria["date"] <= fim)
    ].copy()
    df_filtrado["tempo_relativo"] = (df_filtrado["date"] - inicio).dt.total_seconds()
    return df_filtrado


def adicionar_distancia(df):
    df = df.sort_values("date").copy()
    df["delta_t"] = df["date"].diff().dt.total_seconds().fillna(0)
    df["speed_ms"] = df["speed"] / 3.6
    df["distancia"] = (df["speed_ms"] * df["delta_t"]).cumsum()
    return df


def interpolar(df, dist_comum, coluna):
    return np.interp(dist_comum, df["distancia"], df[coluna])


def calcular_delta(df1, df2, dis_comum):
    tempo1 = np.interp(dis_comum, df1["distancia"], df1["tempo_relativo"])
    tempo2 = np.interp(dis_comum, df2["distancia"], df2["tempo_relativo"])
    return tempo2 - tempo1


def buscar_sessoes(ano):
    url = f"https://api.openf1.org/v1/sessions?year={ano}"
    response = requests.get(url)
    dados = response.json()
    df = pd.DataFrame(dados)
    return df[["session_key", "session_name", "date_start", "circuit_short_name"]]


def buscar_pilotos(session_key):
    url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    response = requests.get(url)
    dados = response.json()
    df = pd.DataFrame(dados)
    return df[["driver_number", "full_name", "team_name"]]

def buscar_anos():
    url = "https://api.openf1.org/v1/sessions"
    response = requests.get(url)
    dados = response.json()
    df = pd.DataFrame(dados)
    df["year"] = pd.to_datetime(df["date_start"], format='mixed').dt.year
    return sorted(df["year"].unique().tolist(), reverse=True)
