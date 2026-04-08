import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="IP Intelligence Tool", layout="wide")

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
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
    margin-top: 1.2rem;
    margin-bottom: 0.6rem;
}

.card {
    background-color: #f8fafc;
    border: 1px solid #d9e2ec;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
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

.badge-high {
    display: inline-block;
    background-color: #fde2e1;
    color: #b42318;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 13px;
}

.badge-medium {
    display: inline-block;
    background-color: #fff1db;
    color: #b54708;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 13px;
}

.badge-low {
    display: inline-block;
    background-color: #e8f7ec;
    color: #027a48;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 13px;
}

.small-label {
    font-size: 12px;
    color: #667085;
    margin-bottom: 4px;
}

.small-value {
    font-size: 18px;
    font-weight: 700;
    color: #17324d;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("IP Intelligence Tool")
st.sidebar.markdown("**Prototype - Fraud Detection**")
st.sidebar.markdown("---")
st.sidebar.write("**Modules**")
st.sidebar.write("- Search")
st.sidebar.write("- Relationship Analysis")
st.sidebar.write("- Risk Scoring")
st.sidebar.markdown("---")
st.sidebar.write("**Environment**")
st.sidebar.write("Mock Data / Demo Version")

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="main-title">IP Intelligence Tool</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Analyze account relationships through shared IP activity, device overlap, and location patterns.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# MOCK DATA
# -----------------------------
accounts_data = pd.DataFrame({
    "Account": ["A10234", "A20456", "A30987", "A45678", "A51234"],
    "Customer Name": ["Carlos M.", "Luis P.", "Ana R.", "Mario G.", "Sofía T."],
    "Primary IP": ["563.123.256.33", "563.123.256.33", "563.123.256.34", "563.123.256.32", "563.123.256.35"],
    "Country": ["Costa Rica", "Perú", "México", "Costa Rica", "Costa Rica"],
    "Device": ["Windows", "Android", "Windows", "iPhone", "Android"],
    "Last Login": ["2026-04-07 08:40", "2026-04-07 09:10", "2026-04-06 23:12", "2026-04-05 19:40", "2026-04-02 10:15"]
})

related_ips_data = pd.DataFrame({
    "IP Address": ["563.123.256.32", "563.123.256.33", "563.123.256.34", "563.123.256.35"],
    "Related Accounts": [3, 5, 2, 1],
    "Last Login": ["2026-04-05 19:40", "2026-04-07 09:10", "2026-04-06 23:12", "2026-04-02 10:15"],
    "Location": ["San José, Costa Rica", "Lima, Perú", "Ciudad de México, México", "San José, Costa Rica"],
    "Shared Devices": [2, 4, 2, 1]
})

related_accounts_detail = pd.DataFrame({
    "Account": ["A10234", "A20456", "A30987", "A45678"],
    "Customer Name": ["Carlos M.", "Luis P.", "Ana R.", "Mario G."],
    "Matched IP": ["563.123.256.33", "563.123.256.33", "563.123.256.34", "563.123.256.32"],
    "Country": ["Costa Rica", "Perú", "México", "Costa Rica"],
    "Device": ["Windows", "Android", "Windows", "iPhone"],
    "Reason for Risk": [
        "Shared IP with multiple accounts",
        "Shared IP + different country",
        "Shared IP + repeated device pattern",
        "Shared IP history"
    ]
})

login_ips_data = pd.DataFrame({
    "IP": ["563.230.092.21", "563.230.092.22", "563.123.256.33", "563.123.256.34", "563.230.092.35"],
    "Last Login": ["2026-04-07 08:22", "2026-04-06 22:12", "2026-04-07 09:10", "2026-04-06 23:12", "2026-04-02 10:15"],
    "Location": [
        "San José, Costa Rica",
        "San José, Costa Rica",
        "Lima, Perú",
        "Ciudad de México, México",
        "San José, Costa Rica"
    ],
    "Device": ["Windows", "Android", "Android", "Windows", "Android"]
})

# -----------------------------
# RISK LOGIC
# -----------------------------
def calculate_risk(related_accounts, shared_devices):
    score = 0

    if related_accounts >= 5:
        score += 50
    elif related_accounts >= 3:
        score += 35
    elif related_accounts >= 2:
        score += 20
    else:
        score += 10

    if shared_devices >= 4:
        score += 25
    elif shared_devices >= 2:
        score += 15
    else:
        score += 5

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return level, score

related_ips_data[["Risk Level", "Risk Score"]] = related_ips_data.apply(
    lambda row: pd.Series(calculate_risk(row["Related Accounts"], row["Shared Devices"])),
    axis=1
)

# -----------------------------
# SEARCH AREA
# -----------------------------
search_col1, search_col2, search_col3 = st.columns([1, 3, 1])

with search_col1:
    search_mode = st.selectbox("Search by", ["Account", "IP"])

with search_col2:
    if search_mode == "Account":
        search_input = st.text_input("Search value", placeholder="Example: A10234")
    else:
        search_input = st.text_input("Search value", placeholder="Example: 563.123.256.33")

with search_col3:
    st.write("")
    st.write("")
    search_button = st.button("Search", use_container_width=True)

# -----------------------------
# HELPERS
# -----------------------------
def risk_badge(level):
    if level == "High":
        return '<span class="badge-high">High Risk</span>'
    elif level == "Medium":
        return '<span class="badge-medium">Medium Risk</span>'
    return '<span class="badge-low">Low Risk</span>'

def highlight_risk(row):
    if row["Risk Level"] == "High":
        return ['background-color: #fde2e1'] * len(row)
    elif row["Risk Level"] == "Medium":
        return ['background-color: #fff1db'] * len(row)
    else:
        return ['background-color: #e8f7ec'] * len(row)

# -----------------------------
# DEFAULT SCREEN
# -----------------------------
if not search_button:
    st.info("Select a search mode, enter an account or IP, and click Search.")

# -----------------------------
# SEARCH RESULTS
# -----------------------------
if search_button and search_input:

    if search_mode == "Account":
        selected_account = accounts_data[
            accounts_data["Account"].str.contains(search_input, case=False, na=False)
        ]
    else:
        selected_account = accounts_data[
            accounts_data["Primary IP"].str.contains(search_input, case=False, na=False)
        ]

    filtered_related_ips = related_ips_data[
        related_ips_data["IP Address"].str.contains(search_input, case=False, na=False)
    ]

    filtered_login_ips = login_ips_data[
        login_ips_data["IP"].str.contains(search_input, case=False, na=False)
    ]

    if search_mode == "Account" and not selected_account.empty:
        primary_ip = selected_account.iloc[0]["Primary IP"]
        filtered_related_ips = related_ips_data[
            related_ips_data["IP Address"].eq(primary_ip)
        ]
        filtered_login_ips = login_ips_data[
            login_ips_data["IP"].eq(primary_ip)
        ]
        filtered_related_accounts = related_accounts_detail[
            related_accounts_detail["Matched IP"].eq(primary_ip)
        ]
    elif search_mode == "IP":
        filtered_related_accounts = related_accounts_detail[
            related_accounts_detail["Matched IP"].str.contains(search_input, case=False, na=False)
        ]
    else:
        filtered_related_accounts = pd.DataFrame()

    # -----------------------------
    # CASE SUMMARY
    # -----------------------------
    st.markdown('<div class="section-title">Case Summary</div>', unsafe_allow_html=True)

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    total_related_ips = len(filtered_related_ips)
    total_related_accounts = len(filtered_related_accounts)
    highest_risk_score = int(filtered_related_ips["Risk Score"].max()) if not filtered_related_ips.empty else 0

    if highest_risk_score >= 70:
        overall_risk = "High"
    elif highest_risk_score >= 40:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"

    with summary_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Related IPs</div>
            <div class="metric-value">{total_related_ips}</div>
        </div>
        """, unsafe_allow_html=True)

    with summary_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Related Accounts</div>
            <div class="metric-value">{total_related_accounts}</div>
        </div>
        """, unsafe_allow_html=True)

    with summary_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Highest Risk Score</div>
            <div class="metric-value">{highest_risk_score}</div>
        </div>
        """, unsafe_allow_html=True)

    with summary_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Risk</div>
            <div style="margin-top: 8px;">{risk_badge(overall_risk)}</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # PROFILE SUMMARY
    # -----------------------------
    st.markdown('<div class="section-title">Profile Summary</div>', unsafe_allow_html=True)

    if not selected_account.empty:
        row = selected_account.iloc[0]

        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            st.markdown(f"""
            <div class="card">
                <div class="small-label">Account</div>
                <div class="small-value">{row["Account"]}</div>

                <div class="small-label">Customer Name</div>
                <div class="small-value">{row["Customer Name"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="card">
                <div class="small-label">Primary IP</div>
                <div class="small-value">{row["Primary IP"]}</div>

                <div class="small-label">Country</div>
                <div class="small-value">{row["Country"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_c:
            st.markdown(f"""
            <div class="card">
                <div class="small-label">Device</div>
                <div class="small-value">{row["Device"]}</div>

                <div class="small-label">Last Login</div>
                <div class="small-value">{row["Last Login"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_d:
            st.markdown(f"""
            <div class="card">
                <div class="small-label">Current Risk Status</div>
                <div style="margin-top: 6px;">{risk_badge(overall_risk)}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No profile summary found for that search value.")

    # -----------------------------
    # RELATED IPS
    # -----------------------------
    st.markdown('<div class="section-title">IPs with Related Accounts</div>', unsafe_allow_html=True)

    if not filtered_related_ips.empty:
        styled_related_ips = filtered_related_ips.style.apply(highlight_risk, axis=1)
        st.dataframe(styled_related_ips, use_container_width=True)
    else:
        st.warning("No related IP records found.")

    # -----------------------------
    # RELATED ACCOUNTS DETAIL
    # -----------------------------
    st.markdown('<div class="section-title">Related Accounts Detail</div>', unsafe_allow_html=True)

    if not filtered_related_accounts.empty:
        st.dataframe(filtered_related_accounts, use_container_width=True)
    else:
        st.warning("No related accounts found.")

    # -----------------------------
    # LOGIN IP HISTORY
    # -----------------------------
    st.markdown('<div class="section-title">Login IP History</div>', unsafe_allow_html=True)

    if not filtered_login_ips.empty:
        st.dataframe(filtered_login_ips, use_container_width=True)
    else:
        st.warning("No login IP history found.")
