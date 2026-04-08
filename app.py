import streamlit as st
import pandas as pd

# ---------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------
st.set_page_config(page_title="IP Intelligence Tool", layout="wide")

# ---------------------------
# ESTILO
# ---------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        color: #12395b;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 16px;
        color: #5c6b7a;
        margin-top: 0;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f4f7fb;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dbe4ee;
        text-align: center;
    }
    .metric-title {
        font-size: 14px;
        color: #5c6b7a;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #12395b;
    }
    .risk-high {
        color: #b42318;
        font-weight: bold;
    }
    .risk-medium {
        color: #d97706;
        font-weight: bold;
    }
    .risk-low {
        color: #15803d;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("IP Intelligence Tool")
st.sidebar.markdown("Prototype - Fraud Detection")
st.sidebar.markdown("---")
st.sidebar.write("**Search Modes**")
st.sidebar.write("- Account")
st.sidebar.write("- IP")
st.sidebar.markdown("---")
st.sidebar.write("**Environment**")
st.sidebar.write("Mock Data / Demo Version")

# ---------------------------
# TÍTULO
# ---------------------------
st.markdown('<p class="main-title">IP Intelligence Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Monitor account relationships through shared IP activity</p>', unsafe_allow_html=True)

# ---------------------------
# DATA MOCK
# ---------------------------
related_ips_data = pd.DataFrame({
    "IP Address": ["563.123.256.32", "563.123.256.33", "563.123.256.34", "563.123.256.35"],
    "Related Accounts": [3, 5, 2, 1],
    "Last Login": ["1/17/2025 01:26PM", "1/10/2026 02:35PM", "1/17/2020 05:11PM", "1/17/2020 01:05PM"],
    "Location": ["San José, Costa Rica", "Lima, Perú", "Ciudad de México, México", "San José, Costa Rica"]
})

login_ips_data = pd.DataFrame({
    "IP": ["563.230.092.21", "563.230.092.22", "563.230.092.02", "563.230.092.15", "563.230.092.35"],
    "Last Login": ["1/17/2020 01:28PM", "1/16/2020 08:12PM", "3/02/2020 12:03AM", "3/4/2018 10:40PM", "1/11/2016 01:01AM"],
    "Location": [
        "San José, Costa Rica",
        "San José, Costa Rica",
        "Alajuela, Costa Rica",
        "Ciudad de México, México",
        "San José, Costa Rica"
    ],
    "Device": ["Windows", "Android", "iPhone", "Windows", "Android"]
})

# ---------------------------
# LÓGICA DE RIESGO
# ---------------------------
def calculate_risk(related_accounts):
    if related_accounts >= 4:
        return "High", 90
    elif related_accounts >= 2:
        return "Medium", 60
    else:
        return "Low", 25

related_ips_data[["Risk Level", "Risk Score"]] = related_ips_data["Related Accounts"].apply(
    lambda x: pd.Series(calculate_risk(x))
)

# ---------------------------
# BUSCADOR
# ---------------------------
st.subheader("Search by Account or IP")
search_input = st.text_input("Type account number or IP", placeholder="Example: 563.123")
search_button = st.button("Search")

# ---------------------------
# FUNCIÓN PARA RESALTAR RIESGO
# ---------------------------
def highlight_risk(row):
    if row["Risk Level"] == "High":
        return ['background-color: #fde2e1'] * len(row)
    elif row["Risk Level"] == "Medium":
        return ['background-color: #fff1db'] * len(row)
    else:
        return ['background-color: #e8f7ec'] * len(row)

# ---------------------------
# RESULTADOS
# ---------------------------
if search_button:
    filtered_related = related_ips_data[
        related_ips_data["IP Address"].str.contains(search_input, case=False, na=False)
    ]

    filtered_login = login_ips_data[
        login_ips_data["IP"].str.contains(search_input, case=False, na=False)
    ]

    total_related_ips = len(filtered_related)
    total_related_accounts = filtered_related["Related Accounts"].sum() if not filtered_related.empty else 0
    highest_risk_score = filtered_related["Risk Score"].max() if not filtered_related.empty else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Related IPs Found</div>
                <div class="metric-value">{total_related_ips}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Total Related Accounts</div>
                <div class="metric-value">{total_related_accounts}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Highest Risk Score</div>
                <div class="metric-value">{highest_risk_score}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("## IPs with Related Accounts")

    if not filtered_related.empty:
        styled_related = filtered_related.style.apply(highlight_risk, axis=1)
        st.dataframe(styled_related, use_container_width=True)
    else:
        st.warning("No related IP results found.")

    st.markdown("## Login IP History")

    if not filtered_login.empty:
        st.dataframe(filtered_login, use_container_width=True)
    else:
        st.warning("No login IP history found.")

else:
    st.info("Enter an account number or IP and click Search.")
