import streamlit as st
import pandas as pd
import boto3
import io

st.set_page_config(page_title="Supply Chain Intelligence", layout="wide")
st.title("🚛 Supply Chain Control Tower")

s3 = boto3.client('s3', endpoint_url='http://localhost:9000',
                  aws_access_key_id='admin', aws_secret_access_key='password123',
                  region_name='us-east-1')

if st.sidebar.button("🔄 Refresh Fleet Data"):
    st.cache_data.clear()

@st.cache_data(ttl=30)
def load_data():
    try:
        response = s3.get_object(Bucket='supply-chain-silver', Key='enriched_shipments.csv')
        return pd.read_csv(io.BytesIO(response['Body'].read()))
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ Waiting for data... Ensure refinery script has finished.")
else:
    # --- DEFENSIVE COLUMN CHECK ---
    for col in ['weather_context', 'location_name', 'temp_alert']:
        if col not in df.columns: df[col] = "Processing..."

    tab1, tab2 = st.tabs(["📍 Precision Tracking", "📊 Fleet Intelligence"])

    with tab1:
        ship_id = st.sidebar.selectbox("Select ID:", sorted(df['shipment_id'].unique()))
        row = df[df['shipment_id'] == ship_id].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Location", row['location_name'])
        c2.metric("Weather", row['weather_context'])
        c3.metric("Temp", f"{row['temperature_c']}°C")
        st.map(df[df['shipment_id'] == ship_id].rename(columns={'latitude': 'lat', 'longitude': 'lon'}))

    with tab2:
        st.subheader("🌐 Fleet Overview")
        st.dataframe(df[['shipment_id', 'location_name', 'status', 'weather_context', 'temperature_c']])