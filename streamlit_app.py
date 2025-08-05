import streamlit as st 
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide"
)

df_data = pd.read_csv("Google-Ads.csv")

df_data['Cost'] = pd.to_numeric(
    df_data['Cost'].replace('[\$,]', '', regex=True), errors='coerce'
).fillna(0)

df_data['Ad_Date'] = pd.to_datetime(df_data['Ad_Date'], dayfirst=True)


st.title("Indicador ADS.📈")

col_graf, col_metrics = st.columns([100, 50])

with col_graf:
    campaign_option= ["Todas"] + list(df_data['Campaign_Name'].unique())
    filtered_campaign = st.selectbox(
        "Selecione a Campanha:",
        campaign_option
    )

    if filtered_campaign != "Todas":
        df_filtered = df_data[df_data['Campaign_Name'] == filtered_campaign]
    else: df_filtered = df_data.copy()


    df_campanhas = df_filtered.groupby('Campaign_Name')['Campaign_Name'].count().reset_index(name='Campanha')
    graf_pizza = px.pie(
        df_campanhas,
        values='Campanha',
        names='Campaign_Name',
        title='Campanhas Ativas'
    )
    st.plotly_chart(graf_pizza, use_container_width=True)

    df_data['Campaign_Name'].unique()
    


with col_metrics:
    total_money = df_filtered['Cost'].sum()
    total_lead = df_filtered['Leads'].sum()

    st.metric(label="Total de Verba Gerenciada", value=f"${int(total_money):,}")
    st.metric(label="Total de Leads Gerados:", value=f"{int(total_lead):,}")


col_uptime, col2 = st.columns(2)

with col_uptime:

    min_date = df_filtered['Ad_Date'].min().date()
    max_date = df_filtered['Ad_Date'].min().date()

    data_range = st.slider(
        label="Período",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )

    star_date = pd.to_datetime(range[0])
    end_date = pd.to_datetime(range[1])

    df_filtered_by_date = df_filtered[(df_filtered['Ad_Date']>= star_date) & (df_filtered['Ad_Date'] <= end_date)]
    
    if not df_filtered_by_date.empty:

        df_filtered_by_date = df_filtered_by_date.sort_values(by='Ad_Date')
        df_custo_por_data = df_filtered_by_date.groupby('Ad_Date')['Cost'].sum().reset_index()

        graf_linha = px.line(
            df_custo_por_data,
            x='Ad_Date',
            y='Cost',
            title='Evolução do Custo no Período Selecionado'
        )
        st.plotly_chart(graf_linha, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para o período selecionado.")