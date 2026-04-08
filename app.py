import streamlit as st
import pandas as pd

# ---------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------
st.set_page_config(page_title="IP Report", layout="wide")

st.title("IP Report")

# ---------------------------
# BUSCADOR
# ---------------------------
st.subheader("Search by Account or IP")

search_input = st.text_input("Type Account or IP")

search_button = st.button("Search")

# ---------------------------
# DATA MOCK (SIMULADA)
# ---------------------------
related_ips_data = pd.DataFrame({
    "IP Address": ["563.123.256.32", "563.123.256.33", "563.123.256.34", "563.123.256.35"],
    "Related Accounts": [3, 3, 2, 1],
    "Last Login": ["1/17/2025 01:26PM", "1/10/2026 02:35PM", "1/17/2020 05:11PM", "1/17/2020 01:05PM"],
    "Details": ["View More", "View More", "View More", "View More"]
})

login_ips_data = pd.DataFrame({
    "IP": ["563.230.092.21", "563.230.092.22", "563.230.092.02", "563.230.092.02", "563.230.092.35"],
    "Last Login": ["1/17/2020 01:28PM", "1/16/2020 08:12PM", "3/02/2020 12:03AM", "3/4/2018 10:40PM", "1/11/2016 01:01AM"],
    "Location": ["San José, Costa Rica"] * 5
})

# ---------------------------
# RESULTADOS
# ---------------------------
if search_button:

    st.markdown("## IPs with Related Accounts")

    # Resaltar filas con riesgo (ej: >=2 cuentas)
    def highlight_rows(row):
        if row["Related Accounts"] >= 2:
            return ['background-color: #f8d7da'] * len(row)
        return [''] * len(row)

    styled_df = related_ips_data.style.apply(highlight_rows, axis=1)

    st.dataframe(styled_df, use_container_width=True)

    st.markdown("### Login IPs")

    st.dataframe(login_ips_data, use_container_width=True)