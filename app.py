import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import base64
from PIL import Image
from html import escape

st.set_page_config(page_title="Intelligence Tool", layout="wide", initial_sidebar_state="expanded")

# Assets are read from the repository directory.
ASSET_DIR = Path(__file__).resolve().parent

@st.cache_data(show_spinner=False)
def asset_base64(filename):
    path = ASSET_DIR / filename
    return base64.b64encode(path.read_bytes()).decode("ascii") if path.is_file() else None

background = asset_base64("Background2.png")

# The background preserves its aspect ratio. The independent logo never stretches.
# For best results Background2.png should contain ONLY the purple gradient.
background_css = (
    f'background-image: url("data:image/png;base64,{background}");'
    if background else
    'background-image: radial-gradient(ellipse at 15% 25%, #73115f 0%, #350742 48%, #160421 100%);'
)
# Load the transparent logo independently from the background.
# Load the PNG through Pillow to ensure consistent rendering in Streamlit.
logo_path = ASSET_DIR / "BASlogo2.png"
if logo_path.is_file():
    try:
        with Image.open(logo_path) as source:
            logo_image = source.convert("RGBA")
        st.logo(logo_image, size="large")
    except Exception as exc:
        st.warning(f"Unable to open BASlogo2.png: {exc}")
else:
    st.warning("BASlogo2.png was not found next to app.py. Check the filename and its location in GitHub.")

st.markdown(f"""
<style>
.stApp {{
    background-color: #190723;
    {background_css}
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stSidebar"] {{
    background: rgba(32, 10, 48, 0.96);
    border-right: 1px solid rgba(255,255,255,0.15);
}}
[data-testid="stSidebar"] * {{ color: white; }}
[data-testid="stMainBlockContainer"] {{
    background: rgba(25, 7, 39, 0.12);
    border-radius: 16px;
    padding-top: 5rem;
}}
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {{ color: white; }}
[data-testid="stMetric"] {{
    background: rgba(65, 24, 85, 0.85);
    padding: 12px;
    border-radius: 10px;
}}
.stButton > button {{ background: #f7f2fb; color: #2a1039; border: 1px solid #e1cde8; }}
.stButton > button p {{ color: #2a1039 !important; }}
</style>
""", unsafe_allow_html=True)

# Application navigation (local demonstration only).
if "active_module" not in st.session_state:
    st.session_state.active_module = "home"

def navigate(module):
    st.session_state.active_module = module
    st.rerun()

with st.sidebar:
    st.title("Intelligence Tool")
    st.caption("Prototype")
    st.divider()
    if st.session_state.active_module != "home":
        if st.button("← Back to Intelligence Tool", key="nav_home_sidebar", use_container_width=True):
            navigate("home")
    if st.session_state.active_module == "ip_report":
        st.write("**IP Report**")
        st.write("**Search Modes**")
        st.write("- By Account")
        st.write("- By IP")
    elif st.session_state.active_module == "avs":
        st.write("**Account Validation System**")
        st.caption("Under Development")
    else:
        st.write("**Applications**")
        st.write("- IP Report")
        st.write("- AVS")
    st.divider()
    st.write("**Environment**")
    st.write("Mock Data / Demo Version 1.0")
    st.caption("Synthetic records only. No external connections.")

if st.session_state.active_module == "home":
    st.markdown("""<style>
    .module-card {background:rgba(65,24,85,.82);border:1px solid rgba(255,255,255,.28);border-radius:16px;padding:28px;min-height:180px;margin-bottom:12px;}
    .module-card h2,.module-card p {color:white !important;}
    </style>""", unsafe_allow_html=True)
    st.title("Intelligence Tool")
    st.subheader("Select an application to continue")
    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="module-card"><h2>IP Report</h2><p>IP address and account relationship analysis</p><p>Demo available</p></div>', unsafe_allow_html=True)
        if st.button("Open IP Report", key="open_ip_report", use_container_width=True):
            navigate("ip_report")
    with right:
        st.markdown('<div class="module-card"><h2>AVS</h2><p>Account Validation System</p><p>Under Development</p></div>', unsafe_allow_html=True)
        if st.button("Open AVS", key="open_avs", use_container_width=True):
            navigate("avs")
    st.caption("Mock Data / Demo Environment")
    st.stop()

if st.session_state.active_module == "avs":
    st.title("AVS")
    st.subheader("Account Validation System")
    st.info("Under Development — This application is not yet available.")
    if st.button("← Back to Intelligence Tool", key="avs_back"):
        navigate("home")
    st.stop()

if st.button("← Back to Intelligence Tool", key="ip_back"):
    navigate("home")

def show_empty_state(message: str):
    """Readable, theme-independent empty result notice."""
    st.markdown(
        '<div style="background:rgba(65,24,85,0.88);'
        'border:1px solid rgba(255,255,255,0.28);'
        'border-radius:9px;padding:15px 18px;margin:10px 0 20px;'
        'color:#ffffff !important;font-size:14px;line-height:1.5;">'
        f'<span style="color:#ffffff !important;">{escape(message)}</span>'
        '</div>',
        unsafe_allow_html=True,
    )

# ---------------------------
# SESSION STATE
# ---------------------------
for key, default in {
    "selected_ip": None,
    "selected_ip_type": None,
    "search_executed": False,
    "last_search_type": "Account",
    "last_search_input": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

for key in [
    "filtered_related_ips",
    "filtered_login_ips",
    "filtered_signup_ips",
    "filtered_login_ip_accounts",
    "filtered_signup_accounts",
    "filtered_related_login_accounts"
]:
    if key not in st.session_state:
        st.session_state[key] = pd.DataFrame()

# ---------------------------
# DATA
# ---------------------------
login_ip_accounts = pd.DataFrame({
    "Account": [
        "A20456","A10234","A30567","A40678",
        "A40023","A40021","A40022","A40024","A99001",
        "A20456","A40023","A51002","A51003",
        "A40023","A70001","A70002",
        "A20456","A40023","A80012","A80014",
        "A40023","A20456","A90022",
        "A20456","A91001","A91002","A91003",
        "A40023","A92001","A92002","A99002",
        "A20456","A93001","A93002","A93003",
        "A40023","A94001","A94002","A94003","A94004"
    ],
    "Customer": [
        "Bad Bunny","Taylor Swift","Ariana Grande","Rihanna",
        "Michael Jackson","Freddie Mercury","Prince","Madonna","Bruno Mars",
        "Bad Bunny","Michael Jackson","Frank Sinatra","Johnny Cash",
        "Michael Jackson","Elton John","Bob Marley",
        "Bad Bunny","Michael Jackson","Jimi Hendrix","James Brown",
        "Michael Jackson","Bad Bunny","Eric Clapton",
        "Bad Bunny","Kendrick Lamar","David Bowie","Mick Jagger",
        "Michael Jackson","Chris Cornell","Axl Rose","Justin Timberlake",
        "Bad Bunny","Bruce Dickinson","Paul McCartney","Roger Waters",
        "Michael Jackson","Lemmy","Ozzy Osbourne","Sebastian Bach","Geddy Lee"
    ],
    "Login IP": [
        "563.123.256.32","563.123.256.32","563.123.256.32","563.123.256.32",
        "563.123.256.33","563.123.256.33","563.123.256.33","563.123.256.33","563.123.256.33",
        "563.123.256.34","563.123.256.34","563.123.256.34","563.123.256.34",
        "563.123.256.35","563.123.256.35","563.123.256.35",
        "563.123.256.36","563.123.256.36","563.123.256.36","563.123.256.36",
        "563.123.256.37","563.123.256.37","563.123.256.37",
        "563.123.256.38","563.123.256.38","563.123.256.38","563.123.256.38",
        "563.123.256.39","563.123.256.39","563.123.256.39","563.123.256.39",
        "563.123.256.40","563.123.256.40","563.123.256.40","563.123.256.40",
        "563.123.256.41","563.123.256.41","563.123.256.41","563.123.256.41","563.123.256.41"
    ],
    "Location": [
        "Lima, Perú","Lima, Perú","Lima, Perú","Lima, Perú",
        "Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala","Guatemala City, Guatemala",
        "Santiago, Chile","Santiago, Chile","Santiago, Chile","Santiago, Chile",
        "Panamá City, Panamá","Panamá City, Panamá","Panamá City, Panamá",
        "Ciudad de México, México","Ciudad de México, México","Ciudad de México, México","Ciudad de México, México",
        "San José, Costa Rica","San José, Costa Rica","San José, Costa Rica",
        "Managua, Nicaragua","Managua, Nicaragua","Managua, Nicaragua","Managua, Nicaragua",
        "Tegucigalpa, Honduras","Tegucigalpa, Honduras","Tegucigalpa, Honduras","Tegucigalpa, Honduras",
        "Quito, Ecuador","Quito, Ecuador","Quito, Ecuador","Quito, Ecuador",
        "San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras","San Pedro Sula, Honduras"
    ],
    "Risk Account": [
        False,False,False,False,
        False,False,False,False,True,
        False,False,True,False,
        False,False,True,
        False,False,False,False,
        False,False,False,
        False,False,True,False,
        False,False,False,True,
        False,False,False,True,
        False,False,False,True,False
    ],
    "Last Login": [
        "2025-01-17","2025-01-17","2025-01-17","2025-01-17",
        "2025-01-20","2025-01-20","2025-01-20","2025-01-20","2025-01-20",
        "2025-02-01","2025-02-01","2025-02-01","2025-02-01",
        "2025-02-10","2025-02-10","2025-02-10",
        "2025-03-05","2025-03-05","2025-03-05","2025-03-05",
        "2025-03-18","2025-03-18","2025-03-18",
        "2025-04-14","2025-04-14","2025-04-14","2025-04-14",
        "2025-05-19","2025-05-19","2025-05-19","2025-05-19",
        "2025-06-02","2025-06-02","2025-06-02","2025-06-02",
        "2025-07-21","2025-07-21","2025-07-21","2025-07-21","2025-07-21"
    ]
})

login_ips_without_relationships = pd.DataFrame({
    "Account": ["A20456","A20456","A20456","A40023","A40023","A40023","A10234","A94003","A70002"],
    "Customer": ["Bad Bunny","Bad Bunny","Bad Bunny","Michael Jackson","Michael Jackson","Michael Jackson","Taylor Swift","Sebastian Bach","Bob Marley"],
    "Login IP": ["563.230.092.22","563.230.092.77","563.230.092.78","563.230.092.41","563.230.092.88","563.230.092.89","563.230.092.21","563.230.092.90","563.230.092.91"],
    "Last Login": ["2025-01-16","2025-02-16","2025-03-10","2025-02-14","2025-06-03","2025-06-15","2025-01-17","2025-07-01","2025-07-04"],
    "Location": ["San José, Costa Rica","Lima, Perú","Quito, Ecuador","Ciudad de México, México","Quito, Ecuador","Panamá City, Panamá","San José, Costa Rica","Guatemala City, Guatemala","Managua, Nicaragua"]
})

signup_ip_accounts = pd.DataFrame({
    "Account": ["A20456","A10234","A30567","A40023","A40021","A99001","A51002","A80013","A94003","A94005"],
    "Customer": ["Bad Bunny","Taylor Swift","Ariana Grande","Michael Jackson","Freddie Mercury","Bruno Mars","Frank Sinatra","Stevie Wonder","Sebastian Bach","Steven Tyler"],
    "Signup IP": ["563.111.111.10","563.111.111.10","563.111.111.10","563.111.111.20","563.111.111.20","563.111.111.20","563.111.111.30","563.111.111.40","563.111.111.50","563.111.111.50"],
    "Country": ["Perú","Ecuador","Honduras","Guatemala","México","Costa Rica","Chile","Rep Dominicana","Honduras","Perú"],
    "Risk Account": [False,False,False,False,False,True,True,True,True,False],
    "Created Date": ["2025-01-05","2025-01-06","2025-01-07","2025-02-10","2025-02-11","2025-02-12","2025-03-01","2025-03-14","2025-04-20","2025-04-22"]
})

# ---------------------------
# HELPERS
# ---------------------------
def add_row_numbers(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    return df

def highlight_risk_row(row):
    if row.get("Risk Account") == True:
        return ['background-color: #f8d7da'] * len(row)
    return [''] * len(row)

def box_style(is_risk: bool) -> str:
    if is_risk:
        return "background-color:#ffc4d1 !important; color:#741029 !important; font-weight:800; border:2px solid #ff315c; padding:8px; border-radius:4px; min-height:42px; display:flex; align-items:center; overflow-wrap:anywhere;"
    return "background-color:transparent !important; color:#ffffff !important; font-weight:500; padding:8px; border-radius:4px; border:1px solid #ddd2e5; min-height:42px; display:flex; align-items:center; overflow-wrap:anywhere;"

# Stable fictional financial values, independent of risk flags.
all_accounts = sorted(set(login_ip_accounts["Account"]) | set(signup_ip_accounts["Account"]) | set(login_ips_without_relationships["Account"]))
ltp_by_account = {account: (1 if i % 2 == 0 else -1) * (750 + i * 3721) for i, account in enumerate(all_accounts)}
ltp_by_account.update({"A20456": 1560, "A40023": -265235, "A51002": 18450, "A51003": -8720})

def format_ltp(value):
    return f"${value:+,}" if value else "$0"

def show_account_table(df, risk_accounts=None, detail_spacing=False):
    """Display account/IP rows using the same Streamlit columns as IP summaries."""
    if df.empty:
        return

    risk_accounts = set(risk_accounts or [])
    display_df = df.copy()
    if "Account" in display_df.columns:
        position = display_df.columns.get_loc("Customer") + 1 if "Customer" in display_df.columns else display_df.columns.get_loc("Account") + 1
        display_df.insert(position, "LTP", display_df["Account"].map(ltp_by_account).map(format_ltp))
    columns = list(display_df.columns)
    # The IP list can be long; give it extra space to remain readable.
    widths = [4 if c == "Shared_IPs" else 2.3 if c in ("Customer", "Location", "Login IP") else 1.5 for c in columns]

    header_cols = st.columns(widths)
    for col, heading in zip(header_cols, columns):
        col.markdown(f"**{escape(str(heading))}**")

    for idx, row in display_df.iterrows():
        account = str(row.get("Account", ""))
        risk_flag = row.get("Risk Account", False)
        # The detail view displays Yes/No strings. bool("No") is True in Python,
        # so explicitly interpret the flag instead of using bool(risk_flag).
        if isinstance(risk_flag, str):
            flagged = risk_flag.strip().lower() in {"yes", "true", "1"}
        else:
            flagged = bool(risk_flag) if pd.notna(risk_flag) else False
        is_risk = flagged or account in risk_accounts
        style = box_style(is_risk)
        if detail_spacing or "Account" in columns:
            # Each cell receives the same bottom margin, creating a visible gap
            # between entire rows without disrupting Streamlit column alignment.
            style += "margin-bottom:10px; min-height:48px; border-radius:7px; "
            if is_risk:
                style += "background-color:#ffc4d1 !important; color:#741029 !important; border:2px solid #ff315c !important; box-shadow:0 0 0 2px rgba(255,49,92,0.30);"
        row_cols = st.columns(widths)
        values = [row[c] for c in columns]
        for col, value in zip(row_cols, values):
            safe_value = escape(str(value)) if pd.notna(value) else ""
            if is_risk and col is row_cols[-1] and "Risk Account" in columns and columns[-1] == "Risk Account":
                safe_value = '<span style="background:#9c1738;color:#fff !important;padding:4px 9px;border-radius:5px;font-weight:800;">HIGH RISK</span>'
            col.markdown(f"<div style='{style}'><span style='color:{'#741029' if is_risk else '#ffffff'} !important;'>{safe_value}</span></div>", unsafe_allow_html=True)

def build_related_ips_summary(filtered_login_accounts):
    if filtered_login_accounts.empty:
        return pd.DataFrame()

    grouped = (
        filtered_login_accounts.groupby("Login IP")
        .agg(
            Related_Accounts=("Account", "nunique"),
            Location=("Location", "first"),
            Has_Risk_Account=("Risk Account", "any")
        )
        .reset_index()
        .rename(columns={
            "Login IP": "IP Address",
            "Related_Accounts": "Related Accounts",
            "Has_Risk_Account": "Has Risk Account"
        })
    )

    grouped = grouped[grouped["Related Accounts"] > 1]
    return grouped.sort_values("IP Address").reset_index(drop=True)

def build_signup_ips_summary(filtered_signup_accounts):
    if filtered_signup_accounts.empty:
        return pd.DataFrame()

    grouped = (
        filtered_signup_accounts.groupby("Signup IP")
        .agg(
            Related_Accounts=("Account", "nunique"),
            Has_Risk_Account=("Risk Account", "any")
        )
        .reset_index()
        .rename(columns={
            "Related_Accounts": "Related Accounts",
            "Has_Risk_Account": "Has Risk Account"
        })
    )

    return grouped.sort_values("Signup IP").reset_index(drop=True)

def show_ip_summary_table(df, ip_column, related_column, info_column=None, has_risk_column="Has Risk Account"):
    st.caption("🔴 Pink rows: IP addresses shared with at least one account flagged as high risk.")
    display_df = add_row_numbers(df)

    if info_column and info_column in display_df.columns:
        header_cols = st.columns([1, 3, 2, 3, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown(f"**{ip_column}**")
        header_cols[2].markdown(f"**{related_column}**")
        header_cols[3].markdown(f"**{info_column}**")
        header_cols[4].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 3, 2])
            style = box_style(bool(row[has_risk_column]))

            row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
            row_cols[1].markdown(f"<div style='{style}'>{row[ip_column]}</div>", unsafe_allow_html=True)
            row_cols[2].markdown(f"<div style='{style}'>{row[related_column]}</div>", unsafe_allow_html=True)
            row_cols[3].markdown(f"<div style='{style}'>{row[info_column]}</div>", unsafe_allow_html=True)

            if row_cols[4].button("View More", key=f"view_{ip_column}_{row[ip_column]}"):
                st.session_state.selected_ip = row[ip_column]
                st.rerun()
    else:
        header_cols = st.columns([1, 3, 2, 2])
        header_cols[0].markdown("**#**")
        header_cols[1].markdown(f"**{ip_column}**")
        header_cols[2].markdown(f"**{related_column}**")
        header_cols[3].markdown("**Details**")

        for idx, row in display_df.iterrows():
            row_cols = st.columns([1, 3, 2, 2])
            style = box_style(bool(row[has_risk_column]))

            row_cols[0].markdown(f"<div style='{style}'>{idx}</div>", unsafe_allow_html=True)
            row_cols[1].markdown(f"<div style='{style}'>{row[ip_column]}</div>", unsafe_allow_html=True)
            row_cols[2].markdown(f"<div style='{style}'>{row[related_column]}</div>", unsafe_allow_html=True)

            if row_cols[3].button("View More", key=f"view_{ip_column}_{row[ip_column]}"):
                st.session_state.selected_ip = row[ip_column]
                st.rerun()

def build_accounts_sharing_multiple_ips(filtered_login_accounts, searched_account):
    if filtered_login_accounts.empty:
        return pd.DataFrame()

    searched_account = searched_account.strip().upper()

    df = filtered_login_accounts[
        filtered_login_accounts["Account"].str.upper() != searched_account
    ]

    grouped = (
        df.groupby(["Account", "Customer"])
        .agg(
            Shared_IP_Count=("Login IP", "nunique"),
            Shared_IPs=("Login IP", lambda x: ", ".join(sorted(set(x))))
        )
        .reset_index()
    )

    grouped = grouped[grouped["Shared_IP_Count"] > 1]
    return grouped

# ---------------------------
# DETAIL PAGE
# ---------------------------
if st.session_state.selected_ip is not None:
    selected_ip = st.session_state.selected_ip

    st.title("IP Detail")
    st.subheader(f"IP: {selected_ip}")

    login_detail_df = login_ip_accounts[
        login_ip_accounts["Login IP"] == selected_ip
    ].copy()

    signup_detail_df = signup_ip_accounts[
        signup_ip_accounts["Signup IP"] == selected_ip
    ].copy()

    login_risk_count = int(login_detail_df["Risk Account"].sum()) if not login_detail_df.empty else 0
    signup_risk_count = int(signup_detail_df["Risk Account"].sum()) if not signup_detail_df.empty else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Login Accounts", len(login_detail_df))

    with c2:
        st.metric("Signup Accounts", len(signup_detail_df))

    with c3:
        st.metric("Risk Accounts", login_risk_count + signup_risk_count)

    st.markdown("## Logins")
    if not login_detail_df.empty:
        login_display = login_detail_df[
            ["Account", "Customer", "Last Login", "Risk Account"]
        ].copy()
        login_display["Risk Account"] = login_display["Risk Account"].map(
            {True: "Yes", False: "No"}
        )
        st.caption("🔴 Pink rows: Accounts flagged as high risk in the prototype data.")
        show_account_table(login_display, risk_accounts=set(
            login_detail_df.loc[login_detail_df["Risk Account"], "Account"]
        ), detail_spacing=True)
    else:
        st.markdown(
            "<div style='background:rgba(65,24,85,0.85);color:#ffffff;"
            "border:1px solid rgba(255,255,255,0.2);padding:12px 16px;"
            "border-radius:6px;'>No login accounts found for this IP.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("## Signup")
    if not signup_detail_df.empty:
        signup_display = signup_detail_df[
            ["Account", "Customer", "Created Date", "Risk Account"]
        ].copy()
        signup_display["Risk Account"] = signup_display["Risk Account"].map(
            {True: "Yes", False: "No"}
        )
        st.caption("🔴 Pink rows: Accounts flagged as high risk in the prototype data.")
        show_account_table(signup_display, risk_accounts=set(
            signup_detail_df.loc[signup_detail_df["Risk Account"], "Account"]
        ), detail_spacing=True)
    else:
        st.markdown(
            "<div style='background:rgba(65,24,85,0.85);color:#ffffff;"
            "border:1px solid rgba(255,255,255,0.2);padding:12px 16px;"
            "border-radius:6px;'>No signup accounts found for this IP.</div>",
            unsafe_allow_html=True,
        )

    if st.button("Back to Search"):
        st.session_state.selected_ip = None
        st.rerun()

# ---------------------------
# MAIN PAGE
# ---------------------------
else:
    top_col1, top_col2 = st.columns([6, 1])

    with top_col1:
        st.title("IP Report")
        st.subheader("Search by Account or IP")



    search_type = st.radio(
        "Search Type",
        ["Account", "IP"],
        horizontal=True,
        index=0 if st.session_state.last_search_type == "Account" else 1
    )

    search_col1, search_col2 = st.columns([2, 2])

    with search_col1:
        search_input = st.text_input(
            "Type Search Value",
            value=st.session_state.last_search_input,
            placeholder="A20456, or 563.123.256.33"
        )

    with search_col2:
        st.date_input(
            "Date Range",
            value=(date(2025, 1, 1), date(2025, 12, 31)),
            help="Visual filter only. Not functional in this prototype version."
        )

    if st.button("Search"):
        st.session_state.last_search_type = search_type
        st.session_state.last_search_input = search_input
        st.session_state.search_executed = True

        search_clean = search_input.strip().upper()

        if search_type == "Account":
            account_login_rows = login_ip_accounts[
                login_ip_accounts["Account"].str.upper() == search_clean
            ]

            account_signup_row = signup_ip_accounts[
                signup_ip_accounts["Account"].str.upper() == search_clean
            ]

            related_ip_matches = account_login_rows["Login IP"].unique().tolist()
            signup_ip_matches = account_signup_row["Signup IP"].unique().tolist()

            signup_ip_as_login_rows = login_ip_accounts[
                login_ip_accounts["Login IP"].isin(signup_ip_matches)
            ]

            signup_ip_as_signup_rows = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].isin(signup_ip_matches)
            ]

            signup_ip_has_login_relation = not signup_ip_as_login_rows.empty
            signup_ip_has_signup_relation = signup_ip_as_signup_rows["Account"].nunique() > 1

            if signup_ip_has_login_relation or signup_ip_has_signup_relation:
                related_ip_matches = list(set(related_ip_matches + signup_ip_matches))

            filtered_related_login_accounts = login_ip_accounts[
                login_ip_accounts["Login IP"].isin(related_ip_matches)
            ]

            signup_related_accounts_for_related_ip = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].isin(related_ip_matches)
            ].rename(columns={
                "Signup IP": "Login IP",
                "Created Date": "Last Login"
            })

            if not signup_related_accounts_for_related_ip.empty:
                signup_related_accounts_for_related_ip["Location"] = signup_related_accounts_for_related_ip["Country"]

                signup_related_accounts_for_related_ip = signup_related_accounts_for_related_ip[
                    ["Account", "Customer", "Login IP", "Location", "Risk Account", "Last Login"]
                ]

                filtered_related_login_accounts = pd.concat(
                    [filtered_related_login_accounts, signup_related_accounts_for_related_ip],
                    ignore_index=True
                )

            filtered_related_ips = build_related_ips_summary(filtered_related_login_accounts)

            filtered_login_ips = login_ips_without_relationships[
                login_ips_without_relationships["Account"].str.upper() == search_clean
            ][["Login IP", "Last Login", "Location"]]

            filtered_signup_accounts_for_summary = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].isin(signup_ip_matches)
            ]

            filtered_signup_ips = build_signup_ips_summary(filtered_signup_accounts_for_summary)

            st.session_state.filtered_related_login_accounts = filtered_related_login_accounts
            st.session_state.filtered_related_ips = filtered_related_ips
            st.session_state.filtered_login_ips = filtered_login_ips
            st.session_state.filtered_signup_ips = filtered_signup_ips

        else:
            filtered_login_ip_accounts = login_ip_accounts[
                login_ip_accounts["Login IP"].str.contains(search_clean, case=False, na=False, regex=False)
            ]

            standalone_login_accounts = login_ips_without_relationships[
                login_ips_without_relationships["Login IP"].str.contains(search_clean, case=False, na=False, regex=False)
            ][["Account", "Customer", "Login IP", "Location", "Last Login"]].copy()

            if not standalone_login_accounts.empty:
                standalone_login_accounts["Risk Account"] = False

                standalone_login_accounts = standalone_login_accounts[
                    ["Account", "Customer", "Login IP", "Last Login", "Risk Account"]
                ]

            filtered_login_ip_accounts = filtered_login_ip_accounts[
                ["Account", "Customer", "Login IP", "Last Login", "Risk Account"]
            ]

            filtered_login_ip_accounts = pd.concat(
                [filtered_login_ip_accounts, standalone_login_accounts],
                ignore_index=True
            )

            filtered_signup_accounts = signup_ip_accounts[
                signup_ip_accounts["Signup IP"].str.contains(search_clean, case=False, na=False, regex=False)
            ]

            st.session_state.filtered_login_ip_accounts = filtered_login_ip_accounts
            st.session_state.filtered_signup_accounts = filtered_signup_accounts

    if st.session_state.search_executed:
        if st.session_state.last_search_type == "Account":
            filtered_related_ips = st.session_state.filtered_related_ips
            filtered_login_ips = st.session_state.filtered_login_ips
            filtered_signup_ips = st.session_state.filtered_signup_ips
            filtered_related_login_accounts = st.session_state.filtered_related_login_accounts

            st.markdown("## Summary")
            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.metric("Total IPs", len(filtered_related_ips) + len(filtered_login_ips) + len(filtered_signup_ips))
            with s2:
                st.metric("IPs with Relationships", len(filtered_related_ips))
            with s3:
                st.metric("Login IPs without Relationships", len(filtered_login_ips))
            with s4:
                st.metric("Signup IP", len(filtered_signup_ips))

            st.markdown("## IPs with Related Accounts")
            if not filtered_related_ips.empty:
                show_ip_summary_table(filtered_related_ips, "IP Address", "Related Accounts", "Location")
            else:
                show_empty_state("No related IPs found.")

            st.markdown("## Accounts Sharing Multiple IPs")
            accounts_sharing_multiple_ips = build_accounts_sharing_multiple_ips(
                filtered_related_login_accounts,
                st.session_state.last_search_input
            )

            if not accounts_sharing_multiple_ips.empty:
                risk_accounts = set(login_ip_accounts.loc[login_ip_accounts["Risk Account"], "Account"]) | set(
                    signup_ip_accounts.loc[signup_ip_accounts["Risk Account"], "Account"]
                )
                st.caption("🔴 Pink rows: Accounts flagged as high risk in the prototype data.")
                show_account_table(accounts_sharing_multiple_ips, risk_accounts)
            else:
                show_empty_state("No other accounts sharing multiple IPs found.")

            st.markdown("## Signup IP")
            if not filtered_signup_ips.empty:
                show_ip_summary_table(filtered_signup_ips, "Signup IP", "Related Accounts")
            else:
                show_empty_state("No signup IP found.")

            st.markdown("## Login IPs without Relationships")
            if not filtered_login_ips.empty:
                risk_accounts = set(login_ip_accounts.loc[login_ip_accounts["Risk Account"], "Account"]) | set(
                    signup_ip_accounts.loc[signup_ip_accounts["Risk Account"], "Account"]
                )
                st.caption("🔴 Pink rows: Accounts flagged as high risk in the prototype data.")
                show_account_table(filtered_login_ips, risk_accounts)
            else:
                show_empty_state("No login IPs without relationships found.")

        else:
            filtered_login_ip_accounts = st.session_state.filtered_login_ip_accounts
            filtered_signup_accounts = st.session_state.filtered_signup_accounts

            st.markdown("## Summary")
            c1, c2 = st.columns(2)

            with c1:
                st.metric("Login IP Accounts", len(filtered_login_ip_accounts))
            with c2:
                st.metric("Signup IP Accounts", len(filtered_signup_accounts))

            st.markdown("## Login IP Accounts")
            if not filtered_login_ip_accounts.empty:
                show_account_table(filtered_login_ip_accounts, detail_spacing=True)
            else:
                show_empty_state("No accounts found using this IP as Login IP.")

            st.markdown("## Signup IP Accounts")
            if not filtered_signup_accounts.empty:
                show_account_table(filtered_signup_accounts, detail_spacing=True)
            else:
                show_empty_state("No accounts found using this IP as Signup IP.")
