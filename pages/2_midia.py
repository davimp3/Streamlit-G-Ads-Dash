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

df_final = df_filtered_by_date.copy()

if filtered_campaign != 'Todas':
        df_final = df_final[df_final['Campaign_Name'] == filtered_campaign]
else: df_final = df_filtered_by_date.copy()



colmetric1,coldevice_type, col4= st.columns([30,30,30])


device_type_option = ["Todos"] + list(df_data['Device'].unique())
filtered_device = st.sidebar.selectbox(
        "Selecione o dispositivo:",
        device_type_option
)


if filtered_device != "Todos":
        df_final = df_final[df_final['Device'] == filtered_device]
else: df_final = df_final.copy()


with coldevice_type:
        df_device = df_final.groupby('Device').size().reset_index(name="Dispositivo")
        pizza_device = px.pie(
                df_device,
                values='Dispositivo',
                names='Device',
                title='Tipo de Dispositivo'
        )

        st.plotly_chart(pizza_device, user_container_width=True)


total_impression = df_final['Impressions'].sum()
total_clicks = df_final['Clicks'].sum()

with colmetric1:

        st.metric(
        label="## Total dsse Impressões:",
        value=f"{(total_impression):,}"
        )


        st.metric(
        label="Total de Cliques:",
        value=f"{(total_clicks):,}"
        )