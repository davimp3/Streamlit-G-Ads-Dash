import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import initialize_session_state
from plotly import graph_objects as go
from datetime import time


initialize_session_state()

st.set_page_config(
    layout  = "wide"
)
st.session_state['ads_data']

empty_right_cl, slider_cl, empty_left_cl = st.columns([20,60,20])

with slider_cl:

    ind_date = st.slider(
        label="Teste",
        min_value=0, 
        max_value=100
    )


left_column, funnel_column, right_column = st.columns([20,40,20])


with left_column:

    fig_h = go.Figure(go.Bar(
            x=[20, 14, 23,12,12,9],
            y=['giraffes', 'orangutans', 'monkeys', 'a', 'b', 'c'],
            orientation='h'))

    st.plotly_chart(fig_h, use_container_width=True)

with funnel_column:


    fig = go.Figure()

    fig.add_trace(go.Funnel(
        name = 'Montreal',
        y = ["Website visit", "Downloads", "Potential customers", "Requested price"],
        x = [120, 60, 30, 20],
        textinfo = "value+percent initial"))

    fig.add_trace(go.Funnel(
        name = 'Toronto',
        orientation = "h",
        y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"],
        x = [100, 60, 40, 30, 20],
        textposition = "inside",
        textinfo = "value+percent previous")) 

    fig.add_trace(go.Funnel(
        name = 'Vancouver',
        orientation = "h",
        y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent", "Finalized"],
        x = [90, 70, 50, 30, 10, 5],
        textposition = "outside",
        textinfo = "value+percent total"))

    st.plotly_chart(fig, use_container_width=True)

    with right_column:
        
        fig_h_r = go.Figure(go.Bar(
            x=[3, 13, 23,12,7,9],
            y=['f', 'g', 'h', 'a', 'b', 'c'],
            orientation='h'))
        
        fig_h_r.update_layout(
            xaxis = dict(autorange="reversed"),
            yaxis = dict(side="right")
        )
        st.plotly_chart(fig_h_r, use_container_width=True)