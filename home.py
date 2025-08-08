import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import initialize_session_state

initialize_session_state()


st.set_page_config(
    layout="wide"
)

df_data = st.session_state['ads_data']

min_date = df_data['Ad_Date'].min().date()
max_date = df_data['Ad_Date'].max().date()

st.sidebar.header("Filtros")
date_range = st.sidebar.slider(
        label="Período",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

df_filtered_by_date = df_data[(df_data['Ad_Date'] >= start_date) & (df_data['Ad_Date']<= end_date)]

st.title("Indicador ADS.📈")

campaign_option= ["Todas"] + list(df_data['Campaign_Name'].unique())
filtered_campaign = st.sidebar.selectbox(
    "Selecione a Campanha:",
    campaign_option
    )

if filtered_campaign != "Todas":
        df_final = df_filtered_by_date[df_filtered_by_date['Campaign_Name'] == filtered_campaign]
else: df_final = df_filtered_by_date.copy()

if df_final.empty:
        st.warning("Não há dados para os filtros selecionados")
else:
        col_graf, col_uptime, col_metrics  = st.columns([60,15,30])

        with col_graf:

            df_campanhas = df_final.groupby('Campaign_Name').size().reset_index(name="Campanha")
            graf_pizza = px.pie(
            df_campanhas,
            values='Campanha',
            names='Campaign_Name',
            title='Campanhas Ativas'
            )
            st.plotly_chart(graf_pizza, use_container_width=True)


        with col_metrics:
            total_money = df_final['Cost'].sum()
            total_lead = df_final['Leads'].sum()

            st.metric(label="Total de Verba Gerenciada", value=f"${int(total_money):,}")
            st.metric(label="Total de Leads Gerados:", value=f"{int(total_lead):,}")
        
        st.divider()

        with col_uptime: 

            df_final_ordenade = df_final.sort_values(by='Ad_Date')
            df_cost_by_date = df_final_ordenade.groupby('Ad_Date')['Cost'].sum().reset_index()

            line_chart = px.line(
            df_cost_by_date,
            x='Ad_Date',
            y='Cost',
            title='Evolução da verba por Período'
            )

        st.plotly_chart(line_chart, use_container_width=True)
