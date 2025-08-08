import streamlit as st
import pandas as pd

def initialize_session_state():
    if'ads_data' not in st.session_state:
        df = pd.read_csv("Google-Ads.csv")

        df['Cost'] = pd.to_numeric(
            df['Cost'].replace('[\$,]', '', regex=True), errors='coerce'
        ).fillna(0)
        df['Ad_Date'] = pd.to_datetime(df['Ad_Date'], dayfirst=True)
        
        st.session_state['ads_data'] = df


