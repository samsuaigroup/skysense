import streamlit as st
import pickle
import numpy as np
import os
from dotenv import load_dotenv

# Load the model
@st.cache_resource
def load_model():
    with open('skysense.pkl', 'rb') as f:
        return pickle.load(f)

st.set_page_config(
    page_title="SkySense - PM2.5 Predictor",
    page_icon="🌍"
)

st.title("🌍 SkySense - Toshkent Havo Sifati Bashorati")
st.markdown("---")

# Load model
model = load_model()

st.subheader("PM2.5 bashorati uchun ma'lumotlarni kiriting")
st.write("AQI indeksi, harorat va namlik qiymatlarini kiriting")

# Create input fields
col1, col2, col3 = st.columns(3)

with col1:
    aqi = st.number_input("AQI indeksi", value=0.0, step=0.1, format="%.2f")

with col2:
    temperature = st.number_input("Harorat (°C)", value=0.0, step=0.1, format="%.2f")

with col3:
    humidity = st.number_input("Namlik (%)", value=0.0, step=0.1, format="%.2f")

if st.button("Bashorat qilish", type="primary"):
    try:
        # Prepare input
        X_test = [[aqi, temperature, humidity]]
        
        # Make prediction
        prediction = model.predict(X_test)[0]
        
        # Display result
        st.success(f"📊 Bashorat qilingan PM2.5: **{prediction:.2f}**")
        
        # Add interpretation
        if prediction < 12:
            st.info("🌱 Havo sifati yaxshi")
        elif prediction < 35.4:
            st.warning("⚠️ Havo sifati o'rtacha")
        elif prediction < 55.4:
            st.error("⚠️⚠️ Havo sifati sezilarli darajada ifloslangan")
        else:
            st.error("🚨 Havo sifati juda yomon")
            
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")

st.markdown("---")
st.caption("SkySense - Sun'iy intellekt yordamida havo sifatini bashorat qilish tizimi")
