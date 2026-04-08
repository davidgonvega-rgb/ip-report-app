import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="IP Intelligence Tool", layout="wide")

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 34px;
    font-weight: 700;
    color: #17324d;
    margin-bottom: 0;
}

.sub-title {
    font-size: 15px;
    color: #667085;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #17324d;
    margin-top: 1.3rem;
    margin-bottom: 0.6rem;
}

.metric-card {
    background-color: #f4f7fb;
    border: 1px solid #d9e2ec;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}

.metric-label {
    font-size: 13px;
    color: #667085;
    margin-bottom: 5px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #17324d;
}

.detail-card {
    background-color: #f8fafc;
    border: 1px solid #d9e2ec;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}

.small-label {
    font-size: 12px;
    color: #667085;
    margin-bottom: 3px;
}

.small-value {
    font-size: 18px;
    font-weight: 700;
    color: #17324d;
    margin-bottom: 12px;
}

.risk-banner {
    background-color: #fde2e1;
    color: #b42318;
    border: 1px solid #f5b5b0;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 700;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("IP Intelligence Tool")
st.sidebar.markdown("**Prototype - Fraud Detection**")
st.sidebar.markdown("---")
st.sidebar.write("**Modules**")
st.sidebar.write("- Search")
st.sidebar.write("- Relationship Analysis")
st.sidebar.write("- IP Detail")
st.sidebar.markdown("---")
st.sidebar.write("**Environment**")
st.sidebar.write("Mock Data / Demo Version")

# ---------------------------------
# HEADER
# ---------------------------------
st.markdown('<div class="main-title">IP Intelligence Tool</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Analyze relationships between customer accounts through login IP activity.</div>',
    unsafe_allow_html=True
)

# ---------------------------------
# MOCK DATA
# ---------------------------------
accounts_data = pd.DataFrame({
    "Account": ["A10234", "A20456", "A30987", "A45678", "A51234", "A67891"],
    "Customer Name": ["Carlos M.", "Luis P.", "Ana R.", "Mario G.", "Sofía T.", "Daniel V."],
    "Primary IP": ["563.123.256.33", "563.123.256.33", "563.123.256.34", "563.123.256.32", "563.230.092.35", "563.123.256.32"],
    "Country": ["Costa Rica", "Perú", "México", "Costa Rica", "Costa Rica", "Guatemala"],
    "Device": ["Windows", "Android", "Windows", "iPhone", "Android", "Windows"],
    "Last Login": ["2026-04-07 08:40", "2026-04-07 09:10", "2026-04-06 23:12", "2026-04-05 19:40", "2026-04-02 10:15", "2026-04-07 11:22"],
    "Is Risk Account": [False, True, False, False, False, True]
})

login_ip_history = pd.DataFrame({
    "Account": ["A10234", "A10234", "A10234", "A20456", "A20456", "A30987", "A45678", "A67891"],
    "IP": [
        "563.123.256.33",
        "563.230.092.21",
        "563.230.092.22",
        "563.123.256.33",
        "563.230.092.77",
        "563.123.256.34",
        "563.123.256.32",
        "563.123.256.32"
    ],
    "Last Login": [
        "2026-04-07 08:40",
        "2026-04-05 13:00",
        "2026-04-01 22:19",
        "2026-04-07 09:10",
        "2026-04-03 16:44",
        "2026-04-06 23:12",
        "2026-04-05 19:40",
        "2026-04-07 11:22"
    ],
    "Location": [
        "Lima, Perú",
        "San José, Costa Rica",
        "Alajuela, Costa Rica",
        "Lima, Perú",
        "Quito, Ecuador",
        "Ciudad de México, México",
        "San José, Costa Rica",
        "Ciudad de Guatemala, Guatemala"
    ],
    "Device": ["Windows", "Windows", "Android", "Android", "Android", "Windows", "iPhone", "Windows"]
})

# ---------------------------------
# BUILD IP SUMMARY TABLE
# ---------------------------------
ip_summary = (
    accounts_data.groupby("Primary IP")
    .agg(
        related_accounts=("Account", "count"),
        last_login=("Last Login", "max")
    )
    .reset_index()
    .rename(columns={"Primary IP": "IP Address"})
)

risk_by_ip = (
    accounts_data.groupby("Primary IP")["Is Risk Account"]
    .any()
    .reset_index()
    .rename(columns={"Primary IP": "IP Address", "Is Risk Account": "Has Risk Relationship"})
)

ip_summary = ip_summary.merge(risk_by_ip, on="IP Address", how="left")

ip_summary["Relationship Type"] = ip_summary["related_accounts"].apply(
    lambda x: "Related Accounts" if x > 1 else "No Relationship"
)

ip_summary["View More"] = ip_summary["related_accounts"].apply(
    lambda x: "View More" if x > 1 else ""
)

# ---------------------------------
# SEARCH AREA
# ---------------------------------
search_col1, search_col2, search_col3 = st.columns([1, 3, 1])

with search_col1:
    search_mode = st.selectbox("Search by", ["Account", "IP"])

with search_col2:
    if search_mode == "Account":
        search_value = st.text_input("Search value", placeholder="Example: A10234")
    else:
        search_value = st.text_input("Search value", placeholder="Example: 563.123.256.33")

with search_col3:
    st.write("")
    st.write("")
    search_button = st.button("Search", use_container_width=True)

# ---------------------------------
# SESSION STATE FOR IP DETAIL
# ---------------------------------
if "selected_ip_detail" not in st.session_state:
    st.session_state.selected_ip_detail = None

# ---------------------------------
# HELPERS
# ---------------------------------
def highlight_relationship_rows(row):
    if row["Has Risk Relationship"]:
        return ['background-color: #fde2e1'] * len(row)
    return [''] * len(row)

# ---------------------------------
# DEFAULT MESSAGE
# ---------------------------------
if not search_button and not st.session_state.selected_ip_detail:
    st.info("Select a search mode, enter an account or IP, and click Search.")

# ---------------------------------
# SEARCH LOGIC
# ---------------------------------
if search_button and search_value:

    # Determine base account(s)
    if search_mode == "Account":
        matched_accounts = accounts_data[
            accounts_data["Account"].str.contains(search_value, case=False, na=False)
        ]
    else:
        matched_accounts = accounts_data[
            accounts_data["Primary IP"].str.contains(search_value, case=False, na=False)
        ]

    if matched_accounts.empty and search_mode == "IP":
        # fallback: search in login history by IP even if not primary IP
        matched_history = login_ip_history[
            login_ip_history["IP"].str.contains(search_value, case=False, na=False)
        ]
        matched_account_ids = matched_history["Account"].unique().tolist()
        matched_accounts = accounts_data[accounts_data["Account"].isin(matched_account_ids)]

    if matched_accounts.empty:
        st.warning("No results found for that search value.")
    else:
        searched_accounts = matched_accounts["Account"].tolist()
        searched_primary_ips = matched_accounts["Primary IP"].unique().tolist()

        account_login_history = login_ip_history[
            login_ip_history["Account"].isin(searched_accounts)
        ].copy()

        all_case_ips = account_login_history["IP"].drop_duplicates().tolist()

        related_ips = ip_summary[
            (ip_summary["IP Address"].isin(all_case_ips)) &
            (ip_summary["related_accounts"] > 1)
        ].copy()

        non_related_login_ips = ip_summary[
            (ip_summary["IP Address"].isin(all_case_ips)) &
            (ip_summary["related_accounts"] == 1)
        ][["IP Address", "last_login"]].copy()

        non_related_login_ips = non_related_login_ips.rename(columns={
            "IP Address": "Login IP",
            "last_login": "Last Login"
        })

        total_ips = len(all_case_ips)
        total_related_ips = len(related_ips)
        total_risk_related_ips = int(related_ips["Has Risk Relationship"].sum()) if not related_ips.empty else 0

        # -----------------------------
        # SUMMARY
        # -----------------------------
        st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total IPs</div>
                <div class="metric-value">{total_ips}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">IPs with Relationships</div>
                <div class="metric-value">{total_related_ips}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Risk-Related IPs</div>
                <div class="metric-value">{total_risk_related_ips}</div>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------
        # RELATED IPS SECTION
        # -----------------------------
        st.markdown('<div class="section-title">IPs with Relationships</div>', unsafe_allow_html=True)

        if not related_ips.empty:
            display_related_ips = related_ips.rename(columns={
                "related_accounts": "Related Accounts",
                "last_login": "Last Login",
                "Has Risk Relationship": "Risk Relationship"
            })[["IP Address", "Related Accounts", "Last Login", "Risk Relationship", "View More"]]

            styled_related = display_related_ips.style.apply(highlight_relationship_rows, axis=1)
            st.dataframe(styled_related, use_container_width=True)

            st.markdown("### Open IP Detail")

            ip_options = related_ips["IP Address"].tolist()
            selected_ip = st.selectbox(
                "Select an IP with relationships to view account detail",
                options=ip_options,
                index=0,
                key="ip_detail_selectbox"
            )

            if st.button("View More Detail"):
                st.session_state.selected_ip_detail = selected_ip

        else:
            st.warning("No relationship IPs found for this case.")

        # -----------------------------
        # NON-RELATED LOGIN IPS
        # -----------------------------
        st.markdown('<div class="section-title">Login IPs without Relationships</div>', unsafe_allow_html=True)

        if not non_related_login_ips.empty:
            st.dataframe(non_related_login_ips, use_container_width=True)
        else:
            st.warning("No login IPs without relationships found.")

# ---------------------------------
# IP DETAIL SCREEN
# ---------------------------------
if st.session_state.selected_ip_detail:
    st.markdown("---")
    st.markdown('<div class="section-title">IP Detail</div>', unsafe_allow_html=True)

    selected_ip = st.session_state.selected_ip_detail

    ip_accounts = accounts_data[accounts_data["Primary IP"] == selected_ip].copy()

    risk_accounts = ip_accounts[ip_accounts["Is Risk Account"] == True]
    normal_accounts = ip_accounts[ip_accounts["Is Risk Account"] == False]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="detail-card">
            <div class="small-label">Selected IP</div>
            <div class="small-value">{selected_ip}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="detail-card">
            <div class="small-label">Linked Accounts</div>
            <div class="small-value">{len(ip_accounts)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="detail-card">
            <div class="small-label">Risk Accounts</div>
            <div class="small-value">{len(risk_accounts)}</div>
        </div>
        """, unsafe_allow_html=True)

    if not risk_accounts.empty:
        st.markdown(
            '<div class="risk-banner">This IP contains one or more risk accounts.</div>',
            unsafe_allow_html=True
        )

    detail_df = ip_accounts.rename(columns={
        "Is Risk Account": "Risk Account"
    })[[
        "Account", "Customer Name", "Country", "Device", "Last Login", "Risk Account"
    ]]

    def highlight_risk_account(row):
        if row["Risk Account"] == True:
            return ['background-color: #fde2e1'] * len(row)
        return [''] * len(row)

    styled_detail_df = detail_df.style.apply(highlight_risk_account, axis=1)
    st.dataframe(styled_detail_df, use_container_width=True)

    if st.button("Close IP Detail"):
        st.session_state.selected_ip_detail = None
        st.rerun()
