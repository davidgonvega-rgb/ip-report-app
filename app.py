import streamlit as st
import pandas as pd

# ---------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------
st.set_page_config(page_title="IP Report", layout="wide")

st.title("IP Report")

# ---------------------------
# ESTADO DE SESIÓN
# ---------------------------
if "selected_ip" not in st.session_state:
    st.session_state.selected_ip = None

# ---------------------------
# BUSCADOR
# ---------------------------
st.subheader("Search by Account or IP")

search_type = st.radio(
    "Search Type",
    ["IP", "Account"],
    horizontal=True
)

search_input = st.text_input(
    "Type search value",
    placeholder="Example: 563.123.256.33 or A10234"
)

search_button = st.button("Search")

# ---------------------------
# DATA MOCK (SIMULADA)
# ---------------------------
related_ips_data = pd.DataFrame({
    "IP Address": ["563.123.256.32", "563.123.256.33", "563.123.256.34", "563.123.256.35"],
    "Related Accounts": [3, 3, 2, 1],
    "Last Login": ["1/17/2025 01:26PM", "1/10/2026 02:35PM", "1/17/2020 05:11PM", "1/17/2020 01:05PM"]
})

login_ips_data = pd.DataFrame({
    "IP": ["563.230.092.21", "563.230.092.22", "563.230.092.02", "563.230.092.02", "563.230.092.35"],
    "Last Login": ["1/17/2020 01:28PM", "1/16/2020 08:12PM", "3/02/2020 12:03AM", "3/4/2018 10:40PM", "1/11/2016 01:01AM"],
    "Location": ["San José, Costa Rica"] * 5
})

# Cuentas relacionadas por IP para el detalle
related_accounts_detail = {
    "563.123.256.32": pd.DataFrame({
        "Account": ["A10234", "A20456", "A30567"],
        "Customer": ["Carlos M.", "Luis P.", "Mario G."],
        "Country": ["Costa Rica", "Perú", "Costa Rica"],
        "Risk Account": [False, True, False]
    }),
    "563.123.256.33": pd.DataFrame({
        "Account": ["A40021", "A40022", "A40023"],
        "Customer": ["Ana R.", "Sofía T.", "Daniel V."],
        "Country": ["México", "Costa Rica", "Guatemala"],
        "Risk Account": [False, False, True]
    }),
    "563.123.256.34": pd.DataFrame({
        "Account": ["A51001", "A51002"],
        "Customer": ["Pedro L.", "María C."],
        "Country": ["Perú", "Costa Rica"],
        "Risk Account": [False, True]
    }),
    "563.123.256.35": pd.DataFrame({
        "Account": ["A70001"],
        "Customer": ["Elena S."],
        "Country": ["Costa Rica"],
        "Risk Account": [False]
    })
}

# Relación cuenta → IPs simulada
account_to_ips = {
    "A10234": ["563.123.256.32", "563.230.092.21"],
    "A20456": ["563.123.256.32", "563.230.092.22"],
    "A40021": ["563.123.256.33"],
    "A40022": ["563.123.256.33"],
    "A40023": ["563.123.256.33"],
    "A51001": ["563.123.256.34"],
    "A51002": ["563.123.256.34"],
    "A70001": ["563.123.256.35"]
}

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def highlight_rows(row):
    if row["Related Accounts"] >= 2:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def highlight_risk_account(row):
    if row["Risk Account"] is True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

# ---------------------------
# MANEJO DE QUERY PARAMS PARA VIEW MORE
# ---------------------------
query_params = st.query_params
if "ip" in query_params:
    st.session_state.selected_ip = query_params["ip"]

# ---------------------------
# RESULTADOS
# ---------------------------
if search_button:
    filtered_related_ips = related_ips_data.copy()
    filtered_login_ips = login_ips_data.copy()

    if search_input.strip():
        if search_type == "IP":
            filtered_related_ips = related_ips_data[
                related_ips_data["IP Address"].str.contains(search_input, case=False, na=False)
            ]
            filtered_login_ips = login_ips_data[
                login_ips_data["IP"].str.contains(search_input, case=False, na=False)
            ]
        else:
            matched_ips = account_to_ips.get(search_input.strip().upper(), [])
            if matched_ips:
                filtered_related_ips = related_ips_data[
                    related_ips_data["IP Address"].isin(matched_ips)
                ]
                filtered_login_ips = login_ips_data[
                    login_ips_data["IP"].isin(matched_ips)
                ]
            else:
                filtered_related_ips = related_ips_data.iloc[0:0]
                filtered_login_ips = login_ips_data.iloc[0:0]

    st.markdown("## IPs with Related Accounts")

    if not filtered_related_ips.empty:
        display_df = filtered_related_ips.copy()

        display_df["Details"] = display_df["IP Address"].apply(
            lambda ip: f"[View More](?ip={ip})"
        )

        display_df = add_row_numbers(display_df)

        styled_df = display_df.style.apply(highlight_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True)

        st.markdown("### Interactive Links")
        for _, row in filtered_related_ips.iterrows():
            st.markdown(f'**{row["IP Address"]}** — [View More](?ip={row["IP Address"]})')
    else:
        st.warning("No related IPs found.")

    st.markdown("### Login IPs")

    if not filtered_login_ips.empty:
        filtered_login_ips = add_row_numbers(filtered_login_ips)
        st.dataframe(filtered_login_ips, use_container_width=True)
    else:
        st.warning("No login IPs found.")

# ---------------------------
# DETALLE DEL IP SELECCIONADO
# ---------------------------
if st.session_state.selected_ip:
    selected_ip = st.session_state.selected_ip

    st.markdown("---")
    st.markdown(f"## IP Detail: {selected_ip}")

    if selected_ip in related_accounts_detail:
        detail_df = related_accounts_detail[selected_ip].copy()
        detail_df = add_row_numbers(detail_df)

        styled_detail_df = detail_df.style.apply(highlight_risk_account, axis=1)
        st.dataframe(styled_detail_df, use_container_width=True)

        st.caption("Rows highlighted in red indicate the risk account.")

        if st.button("Close Detail"):
            st.session_state.selected_ip = None
            st.query_params.clear()
            st.rerun()
    else:
        st.warning("No related account detail found for this IP.")
