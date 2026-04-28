import streamlit as st
import pandas as pd

# ---------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------
st.set_page_config(page_title="IP Report", layout="wide")

# ---------------------------
# HEADER CON LOGO
# ---------------------------

col1, col2 = st.columns([4, 1])

with col2:
    st.image("betcrislogo.png", width=250)



#---------------------------------
# ESTILOS
# ---------------------------



#-------------------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("Betcris")
st.sidebar.title("IP Intelligence Tool")
st.sidebar.markdown("Prototype")
st.sidebar.markdown("---")
st.sidebar.write("**Search Modes**")
st.sidebar.write("- By Account")
st.sidebar.write("- By IP")
st.sidebar.markdown("---")
st.sidebar.write("**Environment**")
st.sidebar.write("Mock Data / Demo Version 1.0")



# ---------------------------
# ESTADO DE SESIÓN
# ---------------------------
if "selected_ip" not in st.session_state:
    st.session_state.selected_ip = None

if "search_executed" not in st.session_state:
    st.session_state.search_executed = False

if "filtered_related_ips" not in st.session_state:
    st.session_state.filtered_related_ips = pd.DataFrame()

if "filtered_login_ips" not in st.session_state:
    st.session_state.filtered_login_ips = pd.DataFrame()

if "filtered_signup_accounts" not in st.session_state:
    st.session_state.filtered_signup_accounts = pd.DataFrame()

if "last_search_type" not in st.session_state:
    st.session_state.last_search_type = "IP"

if "last_search_input" not in st.session_state:
    st.session_state.last_search_input = ""

# ---------------------------
# MOCK DATA DETALLADA POR IP
# ---------------------------
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
        "Account": ["A92001", "A92002"],
        "Customer": ["Silvia H.", "Tatiana Q."],
        "Country": ["Costa Rica", "Nicaragua"],
        "Risk Account": [False, False]
    }),
    "563.123.256.40": pd.DataFrame({
        "Account": ["A93001", "A93002", "A93003"],
        "Customer": ["Fernando D.", "Luis A.", "Paola N."],
        "Country": ["Perú", "Honduras", "Costa Rica"],
        "Risk Account": [False, False, True]
    }),
    "563.123.256.41": pd.DataFrame({
        "Account": ["A94001", "A94002", "A94003", "A94004", "A94005", "A94006"],
        "Customer": ["Rosa M.", "Diego P.", "Camila R.", "Bryan T.", "Natalia S.", "Iván L."],
        "Country": ["Ecuador", "México", "Costa Rica", "Panamá", "Perú", "Guatemala"],
        "Risk Account": [False, False, True, False, False, False]
    })
}

# ---------------------------
# SIGNUP IP ACCOUNTS
# ---------------------------
signup_ip_accounts = pd.DataFrame({
    "Account": [
        "A10234", "A20456", "A40023", "A51002", "A70002",
        "A80013", "A91002", "A93003", "A94003", "A94005"
    ],
    "Customer": [
        "Carlos M.", "Luis P.", "Daniel V.", "María C.", "Roberto N.",
        "Paula M.", "Gloria V.", "Paola N.", "Camila R.", "Natalia S."
    ],
    "Signup IP": [
        "563.123.256.32",
        "563.123.256.32",
        "563.123.256.33",
        "563.123.256.34",
        "563.123.256.35",
        "563.123.256.36",
        "563.123.256.38",
        "563.123.256.40",
        "563.123.256.41",
        "563.123.256.41"
    ],
    "Country": [
        "Costa Rica", "Perú", "Guatemala", "Costa Rica", "Costa Rica",
        "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Perú"
    ],
    "Risk Account": [
        False, True, True, True, True,
        True, True, True, True, False
    ]
})

# ---------------------------
# RESUMEN DE IPS RELACIONADOS
# ---------------------------
ip_last_login_map = {
    "563.123.256.32": "1/17/2025 01:26PM",
    "563.123.256.33": "1/10/2026 02:35PM",
    "563.123.256.34": "1/17/2020 05:11PM",
    "563.123.256.35": "1/17/2020 01:05PM",
    "563.123.256.36": "2/11/2025 09:10AM",
    "563.123.256.37": "3/05/2026 10:22PM",
    "563.123.256.38": "4/14/2025 11:43AM",
    "563.123.256.39": "5/19/2025 08:17PM",
    "563.123.256.40": "6/02/2025 03:09PM",
    "563.123.256.41": "7/21/2025 07:50AM"
}

related_ips_rows = []
for ip, df in related_accounts_detail.items():
    related_ips_rows.append({
        "IP Address": ip,
        "Related Accounts": len(df),
        "Last Login": ip_last_login_map.get(ip, "N/A"),
        "Has Risk Account": bool(df["Risk Account"].any())
    })

related_ips_data = pd.DataFrame(related_ips_rows).sort_values("IP Address").reset_index(drop=True)

# ---------------------------
# LOGIN IPS SIN RELACIÓN
# ---------------------------
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
        "563.230.092.88",
        "563.230.092.99"
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
        "6/03/2025 09:45PM",
        "6/18/2025 07:10AM"
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
        "Quito, Ecuador",
        "Managua, Nicaragua"
    ]
})

# ---------------------------
# RELACIÓN CUENTA -> IPS
# ---------------------------
account_to_ips = {}
for ip, df in related_accounts_detail.items():
    for account in df["Account"].tolist():
        account_to_ips.setdefault(account, []).append(ip)

account_to_ips["A10234"] = account_to_ips.get("A10234", []) + ["563.230.092.21"]
account_to_ips["A20456"] = account_to_ips.get("A20456", []) + ["563.230.092.22"]
account_to_ips["A40023"] = account_to_ips.get("A40023", []) + ["563.230.092.41"]
account_to_ips["A80013"] = account_to_ips.get("A80013", []) + ["563.230.092.55"]
account_to_ips["A94003"] = account_to_ips.get("A94003", []) + ["563.230.092.88"]

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

def highlight_risk_row(row):
    if row["Risk Account"] == True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def box_style(is_risk: bool) -> str:
    if is_risk:
        return "background-color:#f8d7da; padding:8px; border-radius:4px;"
    return "background-color:#ffffff; padding:8px; border-radius:4px; border:1px solid #eee;"

# ---------------------------
# PANTALLA DE DETALLE
# ---------------------------
if st.session_state.selected_ip is not None:
    selected_ip = st.session_state.selected_ip
    st.title("IP Detail")
    st.subheader(f"Linked Accounts for IP: {selected_ip}")

    detail_df = related_accounts_detail.get(selected_ip)

    if detail_df is not None and not detail_df.empty:
        total_accounts = len(detail_df)
        total_risk_accounts = int(detail_df["Risk Account"].sum())

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Linked Accounts", total_accounts)
        with c2:
            st.metric("Risk Accounts", total_risk_accounts)

        st.markdown("### Linked Accounts Detail")
        detail_df = add_row_numbers(detail_df)
        styled_detail_df = detail_df.style.apply(highlight_risk_row, axis=1)
        st.dataframe(styled_detail_df, use_container_width=True)

        st.caption("**Accounts highlighted in red are risk accounts (Either Master or Bonus abusers**).")
    else:
        st.warning("No linked accounts found for this IP.")

    if st.button("Back to Search", key="back_to_search"):
        st.session_state.selected_ip = None
        st.rerun()

# ---------------------------
# PANTALLA PRINCIPAL
# ---------------------------
else:
    st.title("IP Report")
    st.subheader("Search by Account or IP")

    default_index = 0 if st.session_state.last_search_type == "IP" else 1

    search_type = st.radio(
        "Search Type",
        ["IP", "Account"],
        horizontal=True,
        index=default_index
    )

    search_input = st.text_input(
        "Type search value",
        value=st.session_state.last_search_input,
        placeholder="Example: 563.123.256.33 or A10234"
    )

    if st.button("Search"):
        st.session_state.last_search_type = search_type
        st.session_state.last_search_input = search_input
        st.session_state.search_executed = True

        filtered_related_ips = related_ips_data.copy()
        filtered_login_ips = login_ips_data.copy()
        filtered_signup_accounts = pd.DataFrame()

        if search_input.strip():
            if search_type == "IP":
                filtered_related_ips = related_ips_data[
                    related_ips_data["IP Address"].str.contains(search_input, case=False, na=False)
                ]
                filtered_login_ips = login_ips_data[
                    login_ips_data["IP"].str.contains(search_input, case=False, na=False)
                ]
                filtered_signup_accounts = signup_ip_accounts[
                    signup_ip_accounts["Signup IP"].str.contains(search_input, case=False, na=False)
                ]
            else:
                matched_ips = account_to_ips.get(search_input.strip().upper(), [])
                if matched_ips:
                    related_ip_matches = [ip for ip in matched_ips if ip in related_ips_data["IP Address"].tolist()]
                    login_ip_matches = [ip for ip in matched_ips if ip in login_ips_data["IP"].tolist()]

                    filtered_related_ips = related_ips_data[
                        related_ips_data["IP Address"].isin(related_ip_matches)
                    ]
                    filtered_login_ips = login_ips_data[
                        login_ips_data["IP"].isin(login_ip_matches)
                    ]
                else:
                    filtered_related_ips = related_ips_data.iloc[0:0]
                    filtered_login_ips = login_ips_data.iloc[0:0]

        st.session_state.filtered_related_ips = filtered_related_ips
        st.session_state.filtered_login_ips = filtered_login_ips
        st.session_state.filtered_signup_accounts = filtered_signup_accounts

    if st.session_state.search_executed:
        filtered_related_ips = st.session_state.filtered_related_ips
        filtered_login_ips = st.session_state.filtered_login_ips
        filtered_signup_accounts = st.session_state.filtered_signup_accounts

        total_ips = len(filtered_related_ips) + len(filtered_login_ips)
        related_ips_count = len(filtered_related_ips)
        risk_related_ips_count = int(filtered_related_ips["Has Risk Account"].sum()) if not filtered_related_ips.empty else 0

        st.markdown("## Summary")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.metric("Total IPs", total_ips)
        with s2:
            st.metric("IPs with Relationships", related_ips_count)
        with s3:
            st.metric("IPs with Risk Accounts", risk_related_ips_count)

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

                style = box_style(bool(row["Has Risk Account"]))

                row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
                row_cols[1].markdown(f"<div style='{style}'>{row['IP Address']}</div>", unsafe_allow_html=True)
                row_cols[2].markdown(f"<div style='{style}'>{row['Related Accounts']}</div>", unsafe_allow_html=True)
                row_cols[3].markdown(f"<div style='{style}'>{row['Last Login']}</div>", unsafe_allow_html=True)

                if row_cols[4].button("View More", key=f"view_{row['IP Address']}"):
                    st.session_state.selected_ip = row["IP Address"]
                    st.rerun()
        else:
            st.warning("No related IPs found.")

        if st.session_state.last_search_type == "IP":
            st.markdown("### Signup IP Accounts")

            if not filtered_signup_accounts.empty:
                signup_display = add_row_numbers(filtered_signup_accounts)
                styled_signup = signup_display.style.apply(highlight_risk_row, axis=1)
                st.dataframe(styled_signup, use_container_width=True)
                st.caption("Accounts highlighted in red are risk accounts.")
            else:
                st.warning("No signup accounts found for this IP.")

        st.markdown("### Login IPs without Relationships")

        if not filtered_login_ips.empty:
            st.dataframe(add_row_numbers(filtered_login_ips), use_container_width=True)
        else:
            st.warning("No login IPs found.")
