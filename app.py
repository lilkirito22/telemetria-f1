import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from telemetria import (
    buscar_dados_volta,
    buscar_voltas,
    buscar_melhor_volta,
    filtrar_volta,
    adicionar_distancia,
    interpolar,
    calcular_delta,
    buscar_sessoes,
    buscar_pilotos,
    buscar_anos,
)

st.title("F1 Telemetry Dashboard")
st.caption("Driver comparison by distance — real data via OpenF1")

anos = buscar_anos()
ano = st.selectbox("Years", anos)

sessoes = buscar_sessoes(ano)
sessoes["label"] = sessoes["circuit_short_name"] + " — " + sessoes["session_name"]
sessao_selecionada = st.selectbox("Session", sessoes["label"].tolist())

session_key = int(
    sessoes.loc[sessoes["label"] == sessao_selecionada, "session_key"].values[0]
)

pilotos = buscar_pilotos(session_key)
pilotos["label"] = pilotos["full_name"] + " (" + pilotos["team_name"] + ")"
lista_pilotos = pilotos["label"].tolist()

col1, col2 = st.columns(2)
with col1:
    piloto1_label = st.selectbox("Driver 1", lista_pilotos, index=0)
with col2:
    piloto2_label = st.selectbox("Driver 2", lista_pilotos, index=1)

piloto1 = int(pilotos.loc[pilotos["label"] == piloto1_label, "driver_number"].values[0])
piloto2 = int(pilotos.loc[pilotos["label"] == piloto2_label, "driver_number"].values[0])

if st.button("Compare"):
    with st.spinner("Fetching data... this may take a few seconds"):
        df1 = buscar_dados_volta(piloto1, session_key)
        df2 = buscar_dados_volta(piloto2, session_key)
        df1["date"] = pd.to_datetime(df1["date"], format="mixed")
        df2["date"] = pd.to_datetime(df2["date"], format="mixed")

        v1 = buscar_melhor_volta(buscar_voltas(piloto1, session_key))
        v2 = buscar_melhor_volta(buscar_voltas(piloto2, session_key))

        df1 = adicionar_distancia(filtrar_volta(df1, v1))
        df2 = adicionar_distancia(filtrar_volta(df2, v2))

        dist_comum = np.linspace(
            0, min(df1["distancia"].max(), df2["distancia"].max()), 500
        )

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(12, 10))

        ax1.plot(
            dist_comum,
            interpolar(df1, dist_comum, "speed"),
            color="blue",
            label=piloto1_label.split(" (")[0],
        )
        ax1.plot(
            dist_comum,
            interpolar(df2, dist_comum, "speed"),
            color="red",
            label=piloto2_label.split(" (")[0],
        )
        ax1.set_ylabel("Speed (km/h)")
        ax1.legend()

        ax2.plot(dist_comum, interpolar(df1, dist_comum, "throttle"), color="blue")
        ax2.plot(dist_comum, interpolar(df2, dist_comum, "throttle"), color="red")
        ax2.set_ylabel("Throttle (%)")

        ax3.plot(dist_comum, interpolar(df1, dist_comum, "brake"), color="blue")
        ax3.plot(dist_comum, interpolar(df2, dist_comum, "brake"), color="red")
        ax3.set_ylabel("Freio (%)")

        delta = calcular_delta(df1, df2, dist_comum)
        ax4.plot(dist_comum, delta, color="purple")
        ax4.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
        ax4.set_ylabel("Delta (s)")
        ax4.set_title(
            "positive = driver 2 ahead | negative = driver 1 ahead",
            fontsize=9,
            color="gray",
        )

        plt.xlabel("Distance (m)")
        plt.suptitle(f"{sessao_selecionada}", fontsize=13)
        plt.tight_layout()

        st.pyplot(fig)
