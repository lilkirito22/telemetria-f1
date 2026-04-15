# F1 Telemetry Dashboard

[🇧🇷 Português](#português) | [🇬🇧 English](#english)

---

## Português

App web para comparar dados de telemetria de pilotos da F1 com dados reais da OpenF1 API.

### Demo
[Acesse o app aqui]([SEU_LINK_AQUI](https://telemetria-f1-jdrqpuxopmcuetrdgnf6jh.streamlit.app/))

### Funcionalidades
- Selecione qualquer ano, sessão e circuito disponível na OpenF1 API
- Compare dois pilotos lado a lado
- Comparação por distância (não por tempo), permitindo análise ponto a ponto precisa
- Gráficos de velocidade, throttle, freio e delta de tempo
- Dados da volta mais rápida de cada piloto

### Tecnologias
- Python
- Pandas & NumPy — processamento de dados
- Matplotlib — gráficos
- Streamlit — interface web
- OpenF1 API — dados reais de F1

### Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

### O que aprendi
Projeto desenvolvido para aprender Python aplicado à análise de dados de motorsport. Aprendi requisições de API, manipulação de dataframes, interpolação numérica e deploy de aplicações web.

---

## English

Web app for comparing F1 drivers' telemetry data using real race data from the OpenF1 API.

### Demo
[Click here to access the app]([SEU_LINK_AQUI](https://telemetria-f1-jdrqpuxopmcuetrdgnf6jh.streamlit.app/))

### Features
- Select any year, session and circuit available in the OpenF1 API
- Compare any two drivers side by side
- Telemetry comparison based on distance (not time), allowing accurate point-by-point analysis
- Speed, throttle, brake and lap delta charts
- Data from the fastest lap of each driver

### Tech Stack
- Python
- Pandas & NumPy — data processing
- Matplotlib — charts
- Streamlit — web interface
- OpenF1 API — real F1 data

### How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### What I learned
Built this project to learn Python applied to motorsport engineering data analysis. Covered API requests, dataframe manipulation, numerical interpolation and web deployment.
