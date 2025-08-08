import streamlit as st 
import pandas as pd
import plotly.express as px
from data_loader import initialize_session_state

initialize_session_state()

st.set_page_config(
        layout="wide"
)

df_data = st.session_state['ads_data']

min_date= df_data['Ad_Date'].min().date()
max_date= df_data['Ad_Date'].max().date()

st.sidebar.header("Filtros")
data_range = st.sidebar.slider(
        label="Período",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format = "DD/MM/YYYY"
        )

start_date = pd.to_datetime(data_range[0])
end_date = pd.to_datetime(data_range[1])

df_filtered_by_date = df_data[(df_data['Ad_Date'] >= start_date) & (df_data['Ad_Date'] <= end_date)]

st.title("Indicador ADS.📈")

campaign_option = ['Todas'] + list(df_data['Campaign_Name'].unique())
filtered_campaign = st.sidebar.selectbox(
        "Selecione a Campanha:",
        campaign_option
)

if filtered_campaign != 'Todas':
        df_final = df_filtered_by_date[df_filtered_by_date['Campaign_Name'] == filtered_campaign]
else: df_final = df_filtered_by_date.copy()


total_impression = df_final['Impressions'].sum()
total_clicks = df_final['Clicks'].sum()

colmetric1, colmetric2, col3 = st.columns([30,30,40])

with colmetric1:

        st.metric(
        label="## Total dsse Impressões:",
        value=f"{(total_impression):,}"
        )

with colmetric2:
        st.metric(
        label="Total de Cliques:",
        value=f"{(total_clicks):,}"
        )

