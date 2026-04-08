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
    "IP Address": [
        "563.123.256.32",
        "563.123.256.33",
        "563.123.256.34",
        "563.123.256.35",
        "563.123.256.36",
        "563.123.256.37",
        "563.123.256.38",
        "563.123.256.39",
        "563.123.256.40",
        "563.123.256.41"
    ],
    "Related Accounts": [4, 5, 3, 2, 1, 4, 2, 3, 1, 6],
    "Last Login": [
        "1/17/2025 01:26PM",
        "1/10/2026 02:35PM",
        "1/17/2020 05:11PM",
        "1/17/2020 01:05PM",
        "2/11/2025 09:10AM",
        "3/05/2026 10:22PM",
        "4/14/2025 11:43AM",
        "5/19/2025 08:17PM",
        "6/02/2025 03:09PM",
        "7/21/2025 07:50AM"
    ]
})

login_ips_data = pd.DataFrame({
    "IP": [
        "563.230.092.21",
        "563.230.092.22",
        "563.230.092.02",
        "563.230.092.35",
        "563.230.092.41",
        "563.230.092.55",
        "563.230.092.60",
        "563.230.092.71",
        "563.123.256.32",
        "563.123.256.33",
        "563.123.256.36",
        "563.123.256.41"
    ],
    "Last Login": [
        "1/17/2020 01:28PM",
        "1/16/2020 08:12PM",
        "3/02/2020 12:03AM",
        "1/11/2016 01:01AM",
        "2/14/2025 09:50AM",
        "3/08/2025 11:22PM",
        "4/10/2025 05:15PM",
        "5/01/2025 02:18AM",
        "7/02/2025 10:40AM",
        "7/03/2025 11:20AM",
        "7/04/2025 08:55PM",
        "7/05/2025 07:30AM"
    ],
    "Location": [
        "San José, Costa Rica",
        "San José, Costa Rica",
        "Alajuela, Costa Rica",
        "Heredia, Costa Rica",
        "Lima, Perú",
        "Ciudad de México, México",
        "Guatemala City, Guatemala",
        "Panamá City, Panamá",
        "San José, Costa Rica",
        "Lima, Perú",
        "Ciudad de México, México",
        "Quito, Ecuador"
    ]
})

related_accounts_detail = {
    "563.123.256.32": pd.DataFrame({
        "Account": ["A10234", "A20456", "A30567", "A40678"],
        "Customer": ["Carlos M.", "Luis P.", "Mario G.", "Andrea T."],
        "Country": ["Costa Rica", "Perú", "Costa Rica", "Guatemala"],
        "Risk Account": [False, True, False, False]
    }),
    "563.123.256.33": pd.DataFrame({
        "Account": ["A40021", "A40022", "A40023", "A40024", "A40025"],
        "Customer": ["Ana R.", "Sofía T.", "Daniel V.", "Pedro L.", "Melissa C."],
        "Country": ["México", "Costa Rica", "Guatemala", "Perú", "Panamá"],
        "Risk Account": [False, False, True, False, False]
    }),
    "563.123.256.34": pd.DataFrame({
        "Account": ["A51001", "A51002", "A51003"],
        "Customer": ["Pedro L.", "María C.", "Javier F."],
        "Country": ["Perú", "Costa Rica", "México"],
        "Risk Account": [False, True, False]
    }),
    "563.123.256.35": pd.DataFrame({
        "Account": ["A70001", "A70002"],
        "Customer": ["Elena S.", "Roberto N."],
        "Country": ["Costa Rica", "Costa Rica"],
        "Risk Account": [False, True]
    }),
    "563.123.256.36": pd.DataFrame({
        "Account": ["A80011", "A80012", "A80013", "A80014"],
        "Customer": ["Laura G.", "Esteban R.", "Paula M.", "José A."],
        "Country": ["México", "México", "Costa Rica", "Perú"],
        "Risk Account": [False, False, True, False]
    }),
    "563.123.256.37": pd.DataFrame({
        "Account": ["A90021", "A90022"],
        "Customer": ["Kevin B.", "Lucía P."],
        "Country": ["Guatemala", "Guatemala"],
        "Risk Account": [False, False]
    }),
    "563.123.256.38": pd.DataFrame({
        "Account": ["A91001", "A91002", "A91003"],
        "Customer": ["Mauricio C.", "Gloria V.", "Andrés S."],
        "Country": ["Panamá", "Costa Rica", "Ecuador"],
        "Risk Account": [False, True, False]
    }),
    "563.123.256.39": pd.DataFrame({
        "Account": ["A92001"],
        "Customer": ["Silvia H."],
        "Country": ["Costa Rica"],
        "Risk Account": [False]
    }),
    "563.123.256.40": pd.DataFrame({
        "Account": ["A93001"],
        "Customer": ["Fernando D."],
        "Country": ["Perú"],
        "Risk Account": [False]
    }),
    "563.123.256.41": pd.DataFrame({
        "Account": ["A94001", "A94002", "A94003", "A94004", "A94005", "A94006"],
        "Customer": ["Rosa M.", "Diego P.", "Camila R.", "Bryan T.", "Natalia S.", "Iván L."],
        "Country": ["Ecuador", "México", "Costa Rica", "Panamá", "Perú", "Guatemala"],
        "Risk Account": [False, False, True, False, False, False]
    })
}

account_to_ips = {
    "A10234": ["563.123.256.32", "563.230.092.21"],
    "A20456": ["563.123.256.32", "563.230.092.22"],
    "A30567": ["563.123.256.32"],
    "A40678": ["563.123.256.32"],
    "A40021": ["563.123.256.33"],
    "A40022": ["563.123.256.33"],
    "A40023": ["563.123.256.33"],
    "A40024": ["563.123.256.33"],
    "A40025": ["563.123.256.33"],
    "A51001": ["563.123.256.34"],
    "A51002": ["563.123.256.34"],
    "A51003": ["563.123.256.34"],
    "A70001": ["563.123.256.35"],
    "A70002": ["563.123.256.35"],
    "A80011": ["563.123.256.36"],
    "A80012": ["563.123.256.36"],
    "A80013": ["563.123.256.36"],
    "A80014": ["563.123.256.36"],
    "A90021": ["563.123.256.37"],
    "A90022": ["563.123.256.37"],
    "A91001": ["563.123.256.38"],
    "A91002": ["563.123.256.38"],
    "A91003": ["563.123.256.38"],
    "A92001": ["563.123.256.39"],
    "A93001": ["563.123.256.40"],
    "A94001": ["563.123.256.41"],
    "A94002": ["563.123.256.41"],
    "A94003": ["563.123.256.41"],
    "A94004": ["563.123.256.41"],
    "A94005": ["563.123.256.41"],
    "A94006": ["563.123.256.41"]
}

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def highlight_rows(row):
    if row["Related Accounts"] >= 2:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def highlight_risk_account(row):
    if row["Risk Account"] == True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

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
        display_df = add_row_numbers(filtered_related_ips)

        header_cols = st.columns([1, 3, 2, 3, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown("**IP Address**")
        header_cols[2].markdown("**Related Accounts**")
        header_cols[3].markdown("**Last Login**")
        header_cols[4].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 3, 2])

            is_risk_ip = row["Related Accounts"] >= 2
            bg_color = "#f8d7da" if is_risk_ip else "#ffffff"

            row_cols[0].markdown(
                f"<div style='background-color:{bg_color}; padding:8px; border-radius:4px;'>{idx}</div>",
                unsafe_allow_html=True
            )
            row_cols[1].markdown(
                f"<div style='background-color:{bg_color}; padding:8px; border-radius:4px;'>{row['IP Address']}</div>",
                unsafe_allow_html=True
            )
            row_cols[2].markdown(
                f"<div style='background-color:{bg_color}; padding:8px; border-radius:4px;'>{row['Related Accounts']}</div>",
                unsafe_allow_html=True
            )
            row_cols[3].markdown(
                f"<div style='background-color:{bg_color}; padding:8px; border-radius:4px;'>{row['Last Login']}</div>",
                unsafe_allow_html=True
            )

            button_key = f"view_more_{row['IP Address']}"
            if row_cols[4].button("View More", key=button_key):
                st.session_state.selected_ip = row["IP Address"]

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
            st.rerun()
    else:
        st.warning("No related account detail found for this IP.")
