import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.title("IMS Asset Dashboard")

business_id = st.text_input("Enter Business ID")

if st.button("Load Assets"):

    r = requests.get(f"{API}/assets", params={"business_id": business_id})

    if r.status_code == 200:
        assets = pd.DataFrame(r.json())
        st.subheader("Assets")
        st.dataframe(assets)


if st.button("Load Utilisation"):

    r = requests.get(f"{API}/asset-utilisation", params={"business_id": business_id})

    if r.status_code == 200:
        data = pd.DataFrame(r.json())

        st.subheader("Asset Utilisation")
        st.dataframe(data)

        st.bar_chart(data.set_index("asset_code")["utilisation_percent"])
